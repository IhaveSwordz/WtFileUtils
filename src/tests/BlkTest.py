import time

from src.blk.BlkParser import Decoder as BLKDecoder
'''
A good test of BLK performance is to unapck top7500Clans.blk, its a very big blk, doesnt test every datatype though
First Commit BLK code takes about 2.1 seconds.
'''
starttime = time.perf_counter()

with open("testFiles/top7500Clans.blk", "rb") as f:
    raw = f.read()
    decoder = BLKDecoder(raw)
    print(decoder.to_dict())
    print(time.perf_counter()-starttime)