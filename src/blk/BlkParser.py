import zstandard as zstd

from src.blk.FileInfo import FileType
from src.blk.Block import Block
from src.blk.Chunk import ChunkParser, Chunk
from src.blk.ParamParser import BLKTypes
from src.DataHandler import DataHandler


class Decoder:
    """
    a blk parser
    inputs:
    dat: the data to be parsed
    offset: how far along into the data the blk starts
    name_map: an optional parameter for blks that have a name map, see FileInfo.py for more info
    zstd_dict: an optional parameter for blks that have a zstd dict, see FileInfo.py for more info
    """
    def __init__(self, dat, offset=0, name_map:list[bytearray] = None, zstd_dict = None):
        self.data = None
        self.blkType = FileType(dat[0])  # gets blk type, the first byte
        if not self.blkType.is_zstd():
            self.data = DataHandler(dat[1:], offset=offset, read_from_start=False)
        else:
            if self.blkType.needs_dict():
                if zstd_dict is None:
                    print("BAD DICT")
                d = zstd.ZstdCompressionDict(zstd_dict)
                raw = zstd.ZstdDecompressor(d).decompress(dat[1:])
                self.data = DataHandler(raw, offset=offset, read_from_start=False)
            else:
                try:
                    raw = zstd.decompress(dat[1:])
                except zstd.ZstdError:
                    # only done because some zstd data in VROMFS can be in streams instead of standard format
                    x = zstd.ZstdDecompressor().stream_reader(dat[1:])
                    raw = x.read()
                    x.close()
                self.data = DataHandler(raw, offset=offset, read_from_start=False)
        self.names_in_name_map = self.decode_uleb128()  # gets the number of names in the name map
        self.names = None
        if self.blkType.is_slim():
            if name_map is None:
                print("BAD NAME MAP")
            self.names = []
            for name in name_map:
                try:
                    self.names.append(name.decode("utf-8"))
                except UnicodeDecodeError:
                    self.names.append("BADBADBAD"+name.decode("utf-8", errors="ignore"))
        else:
            self.name_map_size = self.decode_uleb128()  # gets the size of the name map
            self.names = [x.decode("utf-8") for x in self.data.fetch(self.name_map_size - 1).split(b"\x00")]
            self.data.advance(1)
            if len(self.names) != self.names_in_name_map:
                print("RED ALERT")
        self.num_of_blocks = self.decode_uleb128()
        self.num_of_params = self.decode_uleb128()
        self.params_data_size = self.decode_uleb128()
        print(self.num_of_blocks, self.num_of_params, self.params_data_size)
        self.params_data = self.data.fetch(self.params_data_size)  # used later on, data
        '''
        here we are are skipping results creation and starting with chunks
        assume we are doing let chunks
        '''
        chunks = []
        parser = ChunkParser(self.names, BLKTypes(self.names, self.params_data))
        for i in range(self.num_of_params):
            chunks.append(parser.parse(self.data.fetch(8)))
        # chunks = Chunks(self.data, self.num_of_params, self.names, B)
        blocks = []
        for i in range(self.num_of_blocks):  # this creates all the blocks
            name_id = self.decode_uleb128()
            param_count = self.decode_uleb128()
            block_count = self.decode_uleb128()
            if block_count > 0:
                first_block_id = self.decode_uleb128()
            else:
                first_block_id = -1
            blocks.append(Block(self.block_id_to_name(name_id), param_count, block_count, first_block_id))

        # if current_t > 0:
        #     print(f"After block creation and final file read: {time.perf_counter() - current_t}")

        result_ptr = 0
        for block in blocks:  # this grabs all the values and puts them in their correct blocks
            field_count = block.param_count
            for i in range(field_count):
                block.add_field(chunks[result_ptr + i])
            result_ptr += field_count

        # if current_t > 0:
        #     print(f"After block param matching: {time.perf_counter() - current_t}")

        self.parent = blocks[0]
        self.from_blocks_with_parent(self.parent, blocks)

        # if current_t > 0:
        #     print(f"After block hierarchy creation: {time.perf_counter() - current_t}")

    def to_dict(self):
        return self.parent.to_dict()

    def decode_uleb128(self):
        """Decodes a ULEB128 encoded value."""
        value = 0
        shift = 0
        while True:
            byte = self.data.fetch(1)[0]
            value |= (byte & 0x7f) << shift
            if not (byte & 0x80):
                break
            shift += 7
        return value

    def block_id_to_name(self, block_id):
        if block_id == 0:
            return "root"
        else:
            return self.names[block_id - 1]

    def from_blocks_with_parent(self, parent, blocks):
        for i in range(parent.blocks_count):
            parent.children.append(blocks[i + parent.first_block_id])
            self.from_blocks_with_parent(blocks[i + parent.first_block_id], blocks)