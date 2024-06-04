# CivMapImagePrep
### ***Turn images into Civ VI maps***
CivMapImagePrep is a Python program designed to transform an input image into a format readable by "Yet not Another Bit-Map Converter" (YnABMC), which is used to create maps for Sid Meier's Civilization VI. This program resizes the image, adjusts the colors to match a predefined set, and formats it appropriately for import into YnABMC.

## Requirements
Python 3.x \
PIL (Pillow) \
[Sid Meier's Civilization VI](https://store.steampowered.com/app/289070/Sid_Meiers_Civilization_VI/) \
[Yet (not) Another Maps Pack](https://github.com/seelingcat/Civ6-YnAMP) \
[YnABMC (Yet *not* Another Bit Map Converter)](https://github.com/Zobtzler/YnABMC)

## Installation
1. Ensure you have Python 3.x installed on your system.
2. Install the required libraries using pip:

## Usage
1. Run the "image_processor.py"
2. Follow the prompts to select an input image, specify the map dimensions, and choose an output directory
3. Wait for the files to save
4. Open YnABMC \
   ![YnABMC on Startup](https://raw.githubusercontent.com/NylonTG/CivMapImagePrep/NylonTG-add--images/images/ynabmcstartup.png)
6. Enter your Map's title in the "Project Name" box
7. Enter your username in the Author box
8. Press "Generate Mod ID"
9. Press "Select Source File" and navigate to where the "IMPORT_INTO_YnABMC.bmp" was saved
10. Uncheck the following options as shown below \
    ![YnABMC open with all the "Import" checkboxes unchecked, Map Supports True Start Location and Real City Naming unchecked, and "Map Generator" next to "Natural Wonders" unchecked](https://raw.githubusercontent.com/NylonTG/CivMapImagePrep/NylonTG-add--images/images/ynabmcsample.png)
11. Press "Generate Map"
12. A folder will be made in the same folder as the .bmp file
13. Copy the folder and paste it in "C:\Users\%userprofile%\Documents\My Games\Sid Meier's Civilization VI\Mods"
14. Start the game and enable the mod
