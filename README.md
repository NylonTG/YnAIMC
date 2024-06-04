# CivMapImagePrep

CivMapImagePrep is a Python program designed to transform an input image into a format readable by "Yet not Another Bit-Map Converter" (YnABMC), which is used to create maps for Sid Meier's Civilization VI. This program resizes the image, adjusts the colors to match a predefined set, and formats it appropriately for import into YnABMC.

## Requirements
Sid Meier's Civilization VI \
Yet (not) Another Maps Pack \
YnABMC (Yet *not* Another Bit Map Converter) \
Python 3.x \
PIL (Pillow) \
Tkinter

## Installation
1. Ensure you have Python 3.x installed on your system.
2. Install the required libraries using pip:

## Usage
1. Run the "image_processor.py"
2. Follow the prompts to select an input image, specify the map dimensions, and choose an output directory.
3. Wait for the files to save
4. Open YnABMC
5. Enter your Map's title in the "Project Name" box
6. Enter your username in the Author box
7. Press "Generate Mod ID"
8. Press "Select Source File" and navigate to where the "IMPORT_INTO_YnABMC.bmp" was saved
9. Uncheck the following options as shown below
10. Press "Generate Map"
11. A folder will be made in the same folder as the .bmp file
12. Copy the folder and paste it in "C:\Users\%userprofile%\Documents\My Games\Sid Meier's Civilization VI\Mods"
13. Start the game and enable the mod
