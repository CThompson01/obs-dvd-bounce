# OBS DVD Bounce

## Description 

This is a script for OBS Studio that bounces a selected source around the screen in the style of DVD logos.

This idea is not my own, this is just my own interpretation of it. Many others have also created scripts to do this.

## Installation

To install, first download the dvd_idle.lua or dvd_idle.py from the releases tab. 
Using Python scripts in OBS requires a bit more setup so if you want the easiest set up I would recommend trying the lua file and if that does not work move on to the Python script.

Store the file in a location where it won't be accidentally deleted, I recommend `C:\Program Files\obs-studio\data\obs-plugins\frontend-tools\scripts` as that is where a couple scripts that are installed by default are located.

Open OBS Studio and go to Tools > Scripts

Under the Scripts tab select the plus sign near the bottom left.

Navigate to where you saved the script and select it.

The script is now ready to go, just select a source!

### Python Installation

If you are going ahead with using the Python script, you must point your OBS to your Python install directory.

To do this, first ensure that you have [Python](https://wiki.python.org/moin/BeginnersGuide/Download) installed.

Once Python is installed, open OBS Studio and navigate to Tools > Scripts

From there, open the tab that says Python Settings.

Under Python Install Path enter in the directory that your Python is installed in. For example 

```
C:/Users/WindowsUser/AppData/Local/Programs/Python/Python311
```

where WindowsUser is your current Windows Account Username and Python311 is your version of Python.

## Configuration

A few configurations are available to the user to allow them to customize the way the source will behave. 

### Update Interval

Changing the update interval will change how frequently the application will move the source.

Increasing this value can cause the animation to look more choppy but can potentially improve performance.

The default value is 10 milliseconds but this setting can be increased to around 50 ms without much of a noticable difference.

### Velocity

Changing the velocity will change how far the source will move every time it gets updated.

Increasing this value can make the animation faster while decreasing it can make it slower. Increasing it too much can cause it to look choppy and will cause it to stay in a very similar pattern. I recommend not increasing it above 100.

The default value is 5.

### Enable/Disable

This option will enable and disable the animation. 
