# WtFileUtils
A module with a set of file utils for extracting and viewing various warthunder file file types

for people finding this on PyPi (and on github aswell I guess) this is very much still a wip, not all planned files 
exist nor are some of them built for module-like use  

# Usage

BLKs:
the blk unpacking class is blk/BlkParser.py/BlkDecoder, as long you pass the blk bin data, the it should work.
current it only supports extraction to JSON like data (a python_dict) using the .to_dict() method

vromfs:
the unpacking class is WtFileUtils/vromfs/VROMFs.py/VROMFs, pass




# Credits
alot of the code here was reverse engineered from the efforts of the people over at 
https://github.com/Warthunder-Open-Source-Foundation 

Without their efforts, I would have had to attempt to reverse engineer Gaijins source code over at https://github.com/GaijinEntertainment/DagorEngine
, which does not sound like a fun time, so thank you to them for their hard work

I also want to thank my friend xCykz who helped me brainstorm

# Notes
if you are looking for a blk / VROMFs unpacker, this is not the place to be. While this project can do so, it will 
not have overhead for cli builtin. This project is more suited to be integrated into projects for VROMFs and blk support.

for a easy-to-use unpacker go look over at https://github.com/Warthunder-Open-Source-Foundation/wt_ext_cli

