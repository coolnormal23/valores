import os
import shutil
import pathlib
import re
import configparser
import stat
import argparse
from rro import remove_readonly

test = 0 #test bit: if 1, copy configuration files from this dir/VALORANT
cfgpath = ""

#cli options
parser = argparse.ArgumentParser()
parser.add_argument("-t","--test", action="store_true", help="Run in test mode")
args = parser.parse_args()
if args.test:
    print("test mode on")
    test = 1

if test == 1:
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

    #nav to config
    cfgpath = dstpath
    cfgpath = os.path.join(cfgpath,"Saved","Config")
else:
    home = os.path.expanduser("~") #%USERPROFILE%
    cfgpath = os.path.join(home,"Appdata","Local","VALORANT","Saved","Config") #\AppData\Local\VALORANT\Saved

#get folders
print("ls for path ",cfgpath)
files = os.listdir(cfgpath)
print(files)

#select user folders
pattern = r'^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}-[a-zA-Z]{2}$'
folders = []
crosshairs = []
for i in files:
    if re.match(pattern,i):
        folders.append(i)
if folders == []:
    shutil.rmtree(dstpath, onerror=remove_readonly)
    raise Exception("You have no user profiles availible to modify. Log into Valorant and try again.")

#get crosshair names
for i in folders:
    userpath = os.path.join(cfgpath,i,"Windows","RiotUserSettings.ini")

    config = configparser.ConfigParser(delimiters='=')
    config.read(userpath)
    name = config.get("Settings","EAresStringSettingName::CrosshairProfileName")
    crosshairs.append(name)

while True: #loop main program logic
    sel=0
    ressel=0

    #Get profile
    print("Valorant user profiles are saved by PUUID (eg:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx-na)")
    print("If you don't know your PUUID, the name of the last used crosshair profile will be provided to help identify which user you are modifying.")
    for i in range(len(folders)):
        print(i,":",folders[i],"(",crosshairs[i],")")
    while True:
        sel = int(input("Choose which user profile to modify:"))
        if sel not in range(len(folders)):
            print("Please select a valid profile.")
        else:
            break

    #check if old ini exists
    oldflag = False
    if "GameUserSettings.ini.old" in os.listdir(os.path.join(cfgpath,folders[sel],"Windows")):
        oldflag = True
        print("Warning! You have already modified this profile. If you proceed, you will overwrite your old saved profile.")
        if input("Is this ok? (y/n): ") != "y":
            print("Exiting.")
            break
    
    # Get GameUserSettings and modify:
    # bShouldLetterbox=False
    # bLastConfirmedShouldLetterbox=False
    # ResolutionSizeX=1280
    # ResolutionSizeY=960
    # LastConfirmedFullscreenMode=2
    # FullscreenMode=2
    userpath = os.path.join(cfgpath,folders[sel],"Windows","GameUserSettings.ini")
    pastepath = os.path.join(cfgpath,folders[sel],"Windows","GameUserSettings.ini.old")
    if oldflag: #remove old file
        os.chmod(pastepath, stat.S_IWRITE) #remove readonly bit
        os.remove(pastepath)
    shutil.copy2(userpath,pastepath) #copy file to old
    os.chmod(userpath, stat.S_IWRITE)   #make file writable if necessary
    gameuserconfig = configparser.ConfigParser(delimiters='=') #create config with = delimiter
    gameuserconfig.optionxform = lambda option: option #enforce case sensitivity
    gameuserconfig.read(userpath)
    resolutions = [(1280,960,"(4:3)"),(1440,1080,"(4:3)"),(1920,1440,"(4:3 for 1440p)"),(1280,1024,"(5:4)")]
    for i in range(len(resolutions)):
        print(i,":",str(resolutions[i][0])+"x"+str(resolutions[i][1]),resolutions[i][2])
    while True:
        ressel = int(input("Choose which resolution to use:"))
        if ressel not in range(len(resolutions)):
            print("Please select a valid profile.")
        else:
            break
    
    gameuserconfig["/Script/ShooterGame.ShooterGameUserSettings"]["bShouldLetterbox"] = "False"
    gameuserconfig["/Script/ShooterGame.ShooterGameUserSettings"]["bLastConfirmedShouldLetterbox"] = "False"
    gameuserconfig["/Script/ShooterGame.ShooterGameUserSettings"]["LastConfirmedFullscreenMode"] = "2"
    gameuserconfig["/Script/ShooterGame.ShooterGameUserSettings"]["FullscreenMode"] = "2"
    gameuserconfig["/Script/ShooterGame.ShooterGameUserSettings"]["ResolutionSizeX"] = str(resolutions[ressel][0])
    gameuserconfig["/Script/ShooterGame.ShooterGameUserSettings"]["ResolutionSizeY"] = str(resolutions[ressel][1])

    #save changes and write without spaces
    with open(userpath, 'w') as configfile:
        for section in gameuserconfig.sections():
            configfile.write(f"[{section}]\n")
            for key, value in gameuserconfig[section].items():
                configfile.write(f"{key}={value}\n")
    os.chmod(userpath, stat.S_IREAD) #make read only
    print("Profile modified.")

    #continue?
    input("Modify another profile? [y/n]: ")
    if input != "y":
        break


if test == 1:
    #remove test dir
    shutil.rmtree(dstpath, onerror=remove_readonly)
    print("Removed test dir ",dstpath)