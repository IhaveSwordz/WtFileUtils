from src.FileSystem.Filesystem import FileSystem


class VROMFsCollection:
    """
    A higher level class compared to VROMFs
    allows to store multiple VROMF objects as well as a combined file system
    also implements auto updating of internal filesystem and vromfs whenever a update happens and data is requested
    :param path: an optional parameter that lets you specify input path(s) to look for vromfs when using func: add
    """
    def __init__(self, path=None):
        self._vromfs = []
        self.Filesystem = FileSystem()
        self.path = None

    def add(self, vromf_path):
