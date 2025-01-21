import os
import stat
import shutil
import pathlib
from rro import remove_readonly
#home = os.path.expanduser("~")

#get paths
ownpath = pathlib.Path(__file__).parent.resolve()
print("Got path: ",ownpath)
srcpath = os.path.join(ownpath,"VALORANT")
print("Got source path: ",srcpath)
dstpath = os.path.join(ownpath,"VALOTEST")
print("Got destination path: ",dstpath)

#copy to test dir
shutil.copytree(srcpath,dstpath)
print("Copied to ",dstpath)

#operations

#remove test dir
shutil.rmtree(dstpath, onerror=remove_readonly)
print("Removed test dir ",dstpath)