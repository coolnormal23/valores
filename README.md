# Valores
[![Linkedin](https://img.shields.io/badge/LinkedIn-blue)](https://www.linkedin.com/in/jakob-edgeworth-a86aa530a/)
[![Personal site](https://img.shields.io/badge/Personal_Site-grey)](https://www.jakobedgeworth.com/)

![valores](https://github.com/coolnormal23/valores/blob/master/asset/valores.png)

A GUI tool to quickly and simply edit your Valorant configuration files on Windows to use stretched resolutions.
### Features
- Modify your resolution for multiple accounts
- Non-destructive: backs up your original configuration file
- Sleek GUI made with Tk and [Sun Valley Theme](https://github.com/rdbende/Sun-Valley-ttk-theme)

# Download and run
## Installation
- Download `valores-1.0.zip` from [Releases](https://github.com/coolnormal23/valores/releases/tag/release)
- Unzip the folder
- Run `valores.exe`
- You may need to unblock the application from antivirus software.
## Usage
- Select a user profile. Your profiles are shown by riot PUUID, followed by your last used crosshair name. You'll have one profile per Riot account you have logged into Valorant with.
- Select a resolution. Included are 1280x960, 1440x1080, 1920x1440, and 1280x1024
- Click apply to save your choices.
- Change your display resolution to match your chosen resolution using Nvidia Control Panel or in Windows under Settings->System->Display.
- Launch the game.

# FAQ
### Valores was detected as a virus by Windows or my antivirus software. Is it safe?
Valores is completely open source and only modifies your game configuration file. Since it modifies files, it may trip your antivirus. If you don't feel safe, you can download the source code and run gui.py yourself, or edit your config yourself with advice [from this Reddit thread](https://www.reddit.com/r/ValorantTechSupport/comments/1gkli2u/comment/lvx1yc7/).
### How can I restore my previous settings?
1. Open your configuration folder. You can use the included button in the application, or navigate to `%LOCALAPPDATA%\AppData\Local\VALORANT\Saved\Config`
2. Open the folder of the profile you changed. Open `Windows`.
3. If don't see `GameUserSettings.ini.old` you're in the wrong profile folder.
4. If you do: Delete your `GameUserSettings.ini`. Rename `GameUserSettings.ini.old` to `GameUserSettings.ini`
