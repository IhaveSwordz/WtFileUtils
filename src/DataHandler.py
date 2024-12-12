import io
import copy


class DataHandler:
    """
    DataHandler handles all data that will be used by the decoder. can be passed either a blob of data (raw hex) or a file
    stream. The functions of the class will handle all grabbing of data and movement of pointer.
    data: can either be a blob of data (raw hex) or a file object gotten from open()
    offset: specifies when in the data to set the pointer
    read_from_start: a boolean that only applies to files, specifies whether to start at the beginning of the file when
    doing file io. if there is a set offset, it goes to the start of the file, then applies the offset

    most common use case is to pass a 'bytes' or 'bytearray' object
    """

    def __init__(self, data, offset: int, read_from_start: bool):
        self._data = data
        self._ptr = offset  # only used when blob
        self._isFile = False
        if type(data) is io.BufferedReader:
            self._isFile = True
            if read_from_start:
                data.seek(offset)
            else:
                data.read(offset)

    '''
    fetches (count) number of bytes from the data source
    '''

    def fetch(self, count: int) -> bytes:
        if self._isFile:
            return self._data.read(count)
        self._ptr += count
        return self._data[self._ptr - count:self._ptr]

    '''
    advances (count) number of bytes from the data source, unlike fetch, it discards any collected data
    '''

    def advance(self, count: int) -> None:
        if self._isFile:
            self._data.read(count)
            return
        self._ptr += count
        return

    def get_rest(self):
        if self._isFile:
            return self._data.read()
        return self._data[self._ptr:]

    def get_ptr(self):
        return copy.deepcopy(self._ptr)

    '''
    function to get next four bytes from the data source and convert it to an int
    '''
    def get_int(self):
        raw = self.fetch(4)
        return int.from_bytes(raw, 'little')

    def get_long(self):
        raw = self.fetch(8)
        return int.from_bytes(raw, 'little')

    def decode_uleb128(self):
        """Decodes a ULEB128 encoded value."""
        value = 0
        shift = 0
        while True:
            byte = self.fetch(1)[0]
            value |= (byte & 0x7f) << shift
            if not (byte & 0x80):
                break
            shift += 7
        return value