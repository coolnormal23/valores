import tkinter as tk
from tkinter import ttk
import os
import shutil
import pathlib
import re
import configparser
import stat
import ctypes
import sv_ttk #theming

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
    ctypes.windll.user32.MessageBoxW(0, "You have no user profiles availible to modify. Log into Valorant and try again.", "Error", 16)
    raise Exception("You have no user profiles availible to modify. Log into Valorant and try again.")

#get crosshair names
for i in folders:
    userpath = os.path.join(cfgpath,i,"Windows","RiotUserSettings.ini")

    config = configparser.ConfigParser(delimiters='=')
    config.read(userpath)
    name = config.get("Settings","EAresStringSettingName::CrosshairProfileName")
    crosshairs.append(name)

def open_conf_loc(): #open config folder location
    os.startfile(os.path.normpath(cfgpath))

def modify(sel,ressel):
    # Get GameUserSettings and modify:
    # bShouldLetterbox=False
    # bLastConfirmedShouldLetterbox=False
    # ResolutionSizeX=1280
    # ResolutionSizeY=960
    # LastConfirmedFullscreenMode=2
    # FullscreenMode=2
    userpath = os.path.join(cfgpath,folders[sel.get()],"Windows","GameUserSettings.ini")
    pastepath = os.path.join(cfgpath,folders[sel.get()],"Windows","GameUserSettings.ini.old")
    oldflag = False
    if "GameUserSettings.ini.old" in os.listdir(os.path.join(cfgpath,folders[sel.get()],"Windows")):
        oldflag = True
    if oldflag is False: #if backup exists
        shutil.copy2(userpath,pastepath) #copy file to old
    os.chmod(userpath, stat.S_IWRITE)   #make file writable if necessary
    gameuserconfig = configparser.ConfigParser(delimiters='=') #create config with = delimiter
    gameuserconfig.optionxform = lambda option: option #enforce case sensitivity
    gameuserconfig.read(userpath)
    
    gameuserconfig["/Script/ShooterGame.ShooterGameUserSettings"]["bShouldLetterbox"] = "False"
    gameuserconfig["/Script/ShooterGame.ShooterGameUserSettings"]["bLastConfirmedShouldLetterbox"] = "False"
    gameuserconfig["/Script/ShooterGame.ShooterGameUserSettings"]["LastConfirmedFullscreenMode"] = "2"
    gameuserconfig["/Script/ShooterGame.ShooterGameUserSettings"]["FullscreenMode"] = "2"
    gameuserconfig["/Script/ShooterGame.ShooterGameUserSettings"]["ResolutionSizeX"] = str(resolutions[ressel.get()][0])
    gameuserconfig["/Script/ShooterGame.ShooterGameUserSettings"]["ResolutionSizeY"] = str(resolutions[ressel.get()][1])

    #save changes and write without spaces
    with open(userpath, 'w') as configfile:
        for section in gameuserconfig.sections():
            configfile.write(f"[{section}]\n")
            for key, value in gameuserconfig[section].items():
                configfile.write(f"{key}={value}\n")
    os.chmod(userpath, stat.S_IREAD) #make read only
    print("Profile modified.")

root = tk.Tk()
root.title("Valores")
mainframe = ttk.Frame(root, padding="3 3 12 12") #main
radioframe = ttk.Frame(root, padding="3 24 12 12") #radiobuttons
radiobuttonsframe = ttk.Frame(radioframe, padding="3 3 12 12")
resolutionframe = ttk.Frame(root,padding="3 24 12 12")
resolutionbuttonsframe = ttk.Frame(resolutionframe, padding="3 3 12 12") #resolutions

radioframe.grid(column=0, row=0)
radiobuttonsframe.grid(column=0, row=1)
resolutionframe.grid(column=1,row=0,rowspan=3)
resolutionbuttonsframe.grid(column=0,row=1)
mainframe.grid(column=0, row=3, columnspan=2)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
ttk.Label(radioframe,text="User Profiles").grid(column=0,row=0)
ttk.Label(resolutionframe,text="Resolutions").grid(column=0,row=0)

radiobuttons = []
radiosel = tk.IntVar() #profile selector
radiosel.set(-1)
for i in range(len(folders)):
    radiobuttons.append(ttk.Radiobutton(radiobuttonsframe,variable=radiosel,value=i,text=folders[i]+" ("+crosshairs[i]+")"))
    radiobuttons[i].grid(column=0,row=i,sticky="nw")
    print("Appended profile radiobutton")

resbuttons = []
ressel = tk.IntVar() #resolution selector
ressel.set(-1)
resolutions = [(1280,960,"(4:3)"),(1440,1080,"(4:3)"),(1920,1440,"(4:3 for 1440p)"),(1280,1024,"(5:4)")]
for i in range(len(resolutions)):
    txt = str(resolutions[i][0]) + "x" + str(resolutions[i][1]) + " " + resolutions[i][2]
    resbuttons.append(ttk.Radiobutton(resolutionbuttonsframe,variable=ressel,value=i,text=txt))
    resbuttons[i].grid(column=0,row=i,sticky="nw")
    print("Appended res radiobutton")

cfgbutton = ttk.Button(mainframe, text="Open Config Location", command=open_conf_loc) #open config
nextbutton = ttk.Button(mainframe, text="Apply", command=lambda: modify(radiosel,ressel),state="disabled") #Next

def checkvar(*args): #enable next if both radiobuttons checked
    if radiosel.get() != -1 and ressel.get() != -1:
        nextbutton.config(state="normal")

radiosel.trace_add("write",checkvar)
ressel.trace_add("write",checkvar)

cfgbutton.grid(column=0,row=0,sticky="nw")
nextbutton.grid(column=1,row=0)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

try: #set icon
    root.iconbitmap("python.ico")
except:
    pass


sv_ttk.set_theme("dark")
root.mainloop()