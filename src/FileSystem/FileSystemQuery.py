from src.FileSystem.File import _BaseFile
from src.Exceptions import FileSystemException


class FileSystemQuery:
    """
    an object used to query a FileSystem / Directory for a specified file
    if supplied a file_obj (an object that inherits _BaseFile), it can also be used to add a file to a directory

    """
    def __init__(self, file, dir_ptr = 0, file_obj = None):
        if isinstance(file, list):
            *self.path, self.name = file
        else:
            *self.path, self.name = file.split('/')
        self.dir_ptr = dir_ptr # value used in file lookup to tell the Directory what path to use for lookup
        self.file_obj: _BaseFile = file_obj


    def get_next(self):
        """
        gets the current path of the query and advances dir_ptr by one
        returns 1, dir_name when supplied a directory
        returns 2, name when at file name
        """
        if self.dir_ptr > len(self.path):
            raise FileSystemException(f'Tried to access a higher level directory than applicable in current FileSystemQuery. Path: {self.path}; Name: {self.name}')
        if self.dir_ptr == len(self.path):
            self.dir_ptr += 1
            return 2, self.name
        else:
            self.dir_ptr += 1
            return 1, self.path[self.dir_ptr-1]


    def get_current(self):
        """
        same as get_next, but doesnt advance dir_ptr
        """
        if self.dir_ptr > len(self.path):
            raise FileSystemException(f'Tried to access a higher level directory than applicable in current FileSystemQuery. Path: {self.path}; Name: {self.name}')
        if self.dir_ptr == len(self.path):
            return 2, self.name
        else:
            return 1, self.path[self.dir_ptr-1]
