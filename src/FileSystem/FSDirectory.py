import os
import traceback

from src.FileSystem.File import _BaseFile
from src.Exceptions import FileSystemException
from src.FileSystem.FileSystemQuery import FileSystemQuery


# noinspection PyTypeChecker
# TODO: implement a recursive backtrace to help display full fs error path in applicable errors
class _FSDirectory:
    """
    one of the classes apart from a file system.
    name: the name of the directory
    parent: used in backtracing to help determine path to base. if its the first directory in the section then set it to None
    """
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent

        """
        The files and directories are stored as dictionaries because it makes lookup and access easier, especially for directories
        """
        self._files: dict[_BaseFile] = {}
        self._directories: dict[FSDirectory] = {}


    def add_file(self, file: _BaseFile | FileSystemQuery):
        """
        supplied with a file, will add it to the current directory

        if supplied with a FileSystemQuery, will navigate through the directories specified and place the file there
        """
        if isinstance(file, FileSystemQuery):
            if file.file_obj is None:
                raise FileSystemException("FileSystemQuery object in add_file missing required attached file (file_obj) object")
            type_, name = file.get_next()
            directory = self._directories.get(name)
            if type_ == 1:
                if directory is None:
                    new_dir = _FSDirectory(name, self)
                    self._directories.update({name: new_dir})
                    new_dir.add_file(file)
                else:
                    directory.add_file(file)

            elif type_ == 2:
                out = self._files.get(name)
                if out is None:
                    self._files.update({name: file.file_obj})
                else:
                    raise FileSystemException("Tried to create a file that already exists")

        if isinstance(file, _BaseFile):
            out = self._files.get(file.file_name)
            if out is None:
                self._files.update({file.file_name: file})
            else:
                raise FileSystemException("Tried to create a file that already exists")

    #TODO: add support for regex and directory lookup.
    def search_file(self, file: FileSystemQuery, suppress_errors = False):
        """
        :param file: a FileSystemQuery object. this class only uses FIleSystemQuery Objects to search for a file
        :param suppress_errors: used to supress any
        :return: the found file, and only if supress_errors is True, sometimes a None
        """
        if not isinstance(file, FileSystemQuery): # error suppression wont ever apply to this
            raise FileSystemException("Passed an invalid argument to search_file")
        type_, name = file.get_next()
        if type_ == 1:
            directory = self._directories.get(name)
            if directory is None and not suppress_errors:
                raise FileSystemException(f"search_file was asked to search an invalid directory with name {name} in {self.name}")
            elif directory is None:
                return None
            return directory.search_file(file)
        elif type_ == 2:
            out = self._files.get(name)
            if out is None and not suppress_errors:
                raise FileSystemException(f"Tried to find a file that doesnt exist in directory {self.name}")
            elif out is None:
                return None
            return out

    # def add_directory(self, directory: FSDirectory):
    #     pass

    def dump(self, spacing=0):
        for f in self._files.values():
            print(" "*spacing, f.file_name)
        for d in self._directories.values():
            print(" "*spacing, d.name + ":")
            d.dump(spacing+2)

    def dump_file(self, base_dir):
        for f in self._files.values():
            with open(base_dir + "/" + f.file_name, "x") as x:
                pass
            with open(base_dir + "/" + f.file_name, "wb") as x:
                try:
                    x.write(f.get_data_disk())
                except Exception as e:
                    stack_trace = traceback.format_exc()
                    disk_trace = self.stack_trace()
                    print(f"ERROR WRITING FILE TO DISK: path: {f.file_name}")
                    print(disk_trace)
                    print("STACK TRACE: ")
                    print(stack_trace)
        for d in self._directories.values():
            try:
                os.mkdir(os.path.join(base_dir, d.name))
            except Exception as e:
                pass
            d.dump_file(os.path.join(base_dir, d.name))

    def stack_trace(self):
        if self.parent is None:
            return [self.name]
        else:
            v = self.parent.stack_trace()
            v.append(self.name)
            return v





class FSDirectory:
    def __init__(self, name):
        self.name = name
        self._files: list[_BaseFile] = []
        self._directories: list[FSDirectory] = []

    '''
    Adds an object (_BaseFile or FSDirectory) to current directory
    both this and fetch abuse custom __eq__ in File.py to allow for easier lookup
    '''

    def add_obj(self, obj):
        if isinstance(obj, FSDirectory):
            if obj in self._directories:
                index = self._directories.index(obj)
                self._directories[index].add_directory(obj._directories)
                self._directories[index].add_file(obj._files)
            else:
                self._directories.append(obj)
        elif isinstance(obj, _BaseFile):
            if obj in self._files:
                raise FileSystemException(f'File {obj} already exists')
                self._files.append(file)
        else:
            raise FileSystemException(f'Object {obj} is not a valid directory / file')

    '''
    given _BaseFile(s), will add them to the current directory
    can take in an input of a single _BaseFile or a list of _BaseFile objects
    if the input contains any object that doesnt inherit BaseFile, it throws an exception
    if the file is already in the directory or a file with the same name exists, a FileSystemException is thrown
    
    '''

    def add_file(self, file: _BaseFile | list[_BaseFile]):
        if not isinstance(file, list):
            file = [file]  # converts it to a list to reduce future processing
        for f in file:
            if isinstance(f, _BaseFile):
                if f not in self._files:
                    self._files.append(f)
                else:
                    raise FileSystemException(f'File {f} already exists')

    '''
    given FSDirectory(s), will add them to the current directory
    if the directory already exists, it will merge the existing and input directory
    
    '''
    #                                : FSDirectory | list[FSDirectory]
    def add_directory(self, directory):
        if not isinstance(directory, list):
            directory = [directory]  # converts it to a list to reduce future processing
        for d in directory:
            if isinstance(d, FSDirectory):
                if d not in self._directories:
                    self._directories.append(d)
                else:
                    index = self._directories.index(d)
                    self._directories[index].add_file(d._files)
                    self._directories[index].add_directory(d._directories)
            else:
                raise FileSystemException(f'Object {d} is not a valid directory')

    '''
    given a FileSystemQuery object
    '''

    def fetch(self, file: FileSystemQuery) -> _BaseFile:
        if len(file) == 1:
            if file[0] in self._files:
                return self._files[self._files.index(file[0])]
            else:
                raise FileSystemException(f'File {file[0]} does not exist')
        else:
            if file[0] in self._directories:
                return self._directories[self._directories.index(file[0])].fetch(file)
            else:
                raise FileSystemException(f'Directory {file[0]} does not exist')

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        if not isinstance(other, FSDirectory):
            return False
        return self.name == other.name
