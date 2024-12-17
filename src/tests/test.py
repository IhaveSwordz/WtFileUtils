import re


with open(r"D:\SteamLibrary\steamapps\common\War Thunder\win64\aces - Copy.exe", "rb") as f:
    data = f.read()

with open("out.bin", "wb") as f:
    for i in re.finditer(re.compile(b"\x00%"), data):
        dat = data[i.start()+1:i.start()+500]
        dat = dat[:dat.find(b"\x00")]
        if b"." in dat:
            f.write(dat)
            f.write(b"\n")