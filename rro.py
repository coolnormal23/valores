import os, stat
import shutil

def remove_readonly(func, path, _):
    #https://docs.python.org/3.11/library/shutil.html#rmtree-example
    "Clear the readonly bit and reattempt the removal"
    os.chmod(path, stat.S_IWRITE)
    func(path)