# OBS DVD Bounce

## Description 

This is a script for OBS Studio that bounces a selected source around the screen in the style of DVD logos.

This idea is not my own, this is just my own interpretation of it. Many others have also created scripts to do this.

## Installation

To install, first download the dvd_idle.py from the releases tab.

Store the file in a location where it won't be accidentally deleted, I recommend `C:\Program Files\obs-studio\data\obs-plugins\frontend-tools\scripts` as that is where a couple scripts that are installed by default are located.

Open OBS Studio and go to Tools > Scripts

Under the Scripts tab select the plus sign near the bottom left.

Navigate to where you saved the script and select it.

The script is now ready to go, just select a source!

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