from src.FileSystem.FSDirectory import FSDirectory
from src.FileSystem.File import _BaseFile
from src.Exceptions import FileSystemException
class FileSystem:
    """
    A FileSystem holds directories.
    A FileSystem does not hold any actual files
    """

    def __init__(self):
        self.main_directory = FSDirectory("base")

    def add_objects(self, directory: FSDirectory):
        pass



    """
    
    given a file path for the vfs, it will scan through the entire file system to find the file and return it
    if no file found, will through a FileSystemException
    th
    """
    def fetch(self, path):
        *directories, file = path.split('/')

