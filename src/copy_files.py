import os
import shutil


def copy_files(source_dir: str, destination_dir: str) -> None:
    src = os.path.abspath(source_dir)
    dst = os.path.abspath(destination_dir)
    if os.path.exists(dst):
        shutil.rmtree(dst)
        print(f"Removed existing contents of '{dst}'")
    os.mkdir(dst)
    contents = os.listdir(src)
    for content in contents:
        src_path = os.path.join(src, content)
        if os.path.isfile(src_path):
            print(f"Copied '{src_path}' to '{shutil.copy(src_path, dst)}'")
        else:
            copy_files(src_path, os.path.join(dst, content))
