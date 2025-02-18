from WtFileUtils.vromfs.VROMFs import VROMFs
from WtFileUtils.FileSystem.FSDirectory import FSDirectory
from WtFileUtils.FileSystem.FileSystemQuery import MassFileSystemQuery
import os
import re


def dump_all(wt_install_path, dump_path, silent=False):
    """
    Dumps all the files from the binary folder (which is the most up to date VROMFS) to dump_path.
    AKA this emulates what most vromfs dumpers do
    MY BLK UNPACKER IS NOT THE FASTEST, SO THIS IS RATHER SLOW (can take a few minutes)
    """
    files = os.listdir(wt_install_path + "/cache")
    input_path = None
    for file in files:
        if file.startswith("binary"):
            input_path = os.path.join(wt_install_path, "cache", file)
            break
    if input_path is None:
        print("unable to find binary path")
    raw_vromfs_files = os.listdir(input_path)
    d = FSDirectory("Base", None)
    for file in raw_vromfs_files:
        temp_path = os.path.join(input_path, file)
        VROMFs(temp_path).get_directory(directory=d)
        print(f"Loaded {temp_path}")
    if not os.path.exists(dump_path):
        os.mkdir(dump_path)
    if os.path.isdir(dump_path):
        d.dump_files(dump_path, skip=True)
    else:
        print("bad file path")
    print("completed")

"""

"""
def lookup(wt_install_path, data_to_lookup, filename_include=None, filename_exclude=None,path_include=None,path_exclude=None):
    """
    A function to look up files that contain certain data
    you can apply filters to the searched files based on name and path
    for all searches, if you supply a compiled re (re.Pattern) object, it will do a re match instead of a (if x in y) match
    all files are bytes, not strings, so you must use b""

    :param wt_install_path: the warthunder installation path
    :param data_to_lookup: what value(s) to look up in the file
    :param filename_include:
    :param filename_exclude:
    :param path_include:
    :param path_exclude:
    :return:
    """
    if not isinstance(data_to_lookup, list):
        data_to_lookup = [data_to_lookup]
    files = os.listdir(wt_install_path + "/cache")
    input_path = None
    for file in files:
        if file.startswith("binary"):
            input_path = os.path.join(wt_install_path, "cache", file)
            break
    if input_path is None:
        print("unable to find binary path")
    raw_vromfs_files = os.listdir(input_path)
    d = FSDirectory("Base", None)
    for file in raw_vromfs_files:
        temp_path = os.path.join(input_path, file)
        VROMFs(temp_path).get_directory(directory=d)
        print(f"Loaded {temp_path}")

    m = MassFileSystemQuery(path_include, path_exclude, filename_include, filename_exclude)
    for f in d.search_for_files(m):
        f_data = f[1].get_data()
        for m in data_to_lookup:
            if isinstance(m, bytes):
                if m in f_data:
                    print('/'.join(f[0]))
                    break
            if isinstance(m, re.Pattern):
                if m.match(f_data) is not None:
                    print('/'.join(f[0]))


    # print(type(re.compile(".*"))), <class 're.Pattern'>


if __name__ == '__main__':
    path = r"D:\SteamLibrary\steamapps\common\War Thunder"
    # dump_all(path, "dump", silent=True)
    lookup(path, b"hotkeys/ID_CAMERA_FOLLOW_OBJECT", filename_exclude=re.compile(".*\.blk$"))

    # file = r"C:\Program Files (x86)\Steam\steamapps\content\app_236390\depot_236391\aces.vromfs.bin"
    # vromf = VROMFs(file)
    # with open("dump.bin", "wb") as f:
    #     f.write(zlib.decompress(_RawData(file).inner_data))
    # file = r"D:\SteamLibrary\steamapps\common\War Thunder\cache\binary.2.41.0\gui.vromfs.bin"
    # vromf = VROMFs(file)
    # for f in vromf._get_file_data():
    #     print(f.true_name)
    r'''
    files = os.listdir(r"D:\SteamLibrary\steamapps\common\War Thunder\cache\binary.2.43.0")
    d = FSDirectory("Base", None)
    #vromf = VROMFs(r"D:\SteamLibrary\steamapps\common\War Thunder\cache\binary.2.43.0\char.vromfs.bin")
    vromf = VROMFs(r"D:\SteamLibrary\steamapps\common\War Thunder\ui\atlases.vromfs.bin")

    # d = vromf.get_directory()
    # file = d.search_file(FileSystemQuery(["config", "wpcost.blk"]))
    # print(file.get_data())
    # d = vromf.get_directory()
    # d.dump_file(r"C:\Users\samue\PycharmProjects\WtFileUtils\WtFileUtils\FileSystem\output\fonts")
    # print("Dumped")
    # input()

    for c in files:
        c = r"D:\SteamLibrary\steamapps\common\War Thunder\cache\binary.2.43.0" + "\\" + c
        vromf = VROMFs(c)
        vromf.get_directory(directory=d)
        print(c)
        # if c == r"D:\SteamLibrary\steamapps\common\War Thunder\cache\binary.2.43.0\gui.vromfs.bin":
        #     z = vromf.get_directory()
           #  z.dump_file("out")
        z = re.compile(b"NET_UNIT_SEVERE_DAMAGE")
        for f in vromf._get_file_data():
            #  print(f.true_name)
            # if "us_m3_lee" in '/'.join(f.true_name):
            #    print(f.true_name)

            if not f.file_name.endswith(".blk"):
                if len(list(z.finditer(f.get_data()))) > 0:
                    print(f.true_name)
    # d.dump_files("out")
                # if b"hitsAnalisys" in f.get_data():
                #     print(f.true_name)
                    # with open(f.file_name, "wb") as z:
                    #     z.write(f.get_data())
    # d.dump_file(r"C:\Users\samue\PycharmProjects\WtFileUtils\WtFileUtils\FileSystem\output\test")
        # for f in vromf._get_file_data():
        #     if f.file_name.endswith(".nut"):
        #         print(f.true_name)
        # f b"isTanksAllowed" in f.get_data():
        #     print(f.true_name)

    # print(vromf.version.get_data())
    #     if b"domination" in f.get_data():
    #         print(f.true_name)
            # with open(f"output/{f.file_name}", "wb") as x:
            #     x.write(f.get_data())

        # if f.file_name.endswith(".nut"):
        #     if b"KILLED" in f.get_data():
        #         print(f.true_name)

            # print(json.dumps(vromf.open_file(f).to_dict(), indent=2, ensure_ascii=False))
            # print(vromf.open_file_raw(f))'''
