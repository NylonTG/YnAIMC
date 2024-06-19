from PIL import Image
from tkinter import filedialog, messagebox, simpledialog
import random
import string
import shutil
import os

# Constants
output_dir = filedialog.askdirectory(
        title="Select Output Directory"
    )

INPUT_IMAGE = os.path.join(output_dir, "color_corrected_map.bmp")
TERRAIN_DICT = {
    (32, 192, 64): "GRASS",
    (192, 224, 0): "PLAINS",
    (224, 128, 0): "DESERT",
    (192, 220, 192): "TUNDRA",
    (255, 255, 255): "SNOW",
    (0, 160, 192): "COAST",
    (64, 64, 192): "OCEAN"
}

# Load the image
try:
    image = Image.open(INPUT_IMAGE)
except IOError as e:
    print(f"Error opening image: {e}")
    exit(1)

# Get user input
title = input("Give your map a name (a variety of different letters are supported, beyond A-Z and 0-9): ")
author = input("Enter your username or whatever name you want to be attributed to your map: ")
length, height = image.size


# Generate a unique mod ID
def generate_mod_id(length=32):
    characters = string.ascii_lowercase + string.digits
    random_id = ''.join(random.choices(characters, k=length))
    return f"{random_id[:8]}-{random_id[8:12]}-{random_id[12:16]}-{random_id[16:20]}-{random_id[20:]}"


mod_id = generate_mod_id()

# Create required folders
folders = [os.path.join(output_dir, f"{author}_{title}/{sub_folder}") for sub_folder in ['Config', 'Lua', 'Map']]
for folder in folders:
    os.makedirs(folder, exist_ok=True)


# Get the terrain type from pixel color
def get_pix(x, y):
    rgb = image.getpixel((x, y))
    return TERRAIN_DICT.get(rgb, "UNKNOWN")


# Replace placeholders in template files
def replace_words(input_file, output_file, replacements):
    try:
        shutil.copyfile(input_file, output_file)

        with open(output_file, 'r') as file:
            content = file.read()

        for old_word, new_word in replacements.items():
            content = content.replace(old_word, new_word)

        with open(output_file, 'w') as file:
            file.write(content)

        if input_file.endswith('_Map.lua'):
            with open(output_file, 'a') as file:
                for y in range(height):
                    for x in range(length):
                        terrain = get_pix(x, y)
                        file.write(
                            f'\nMapToConvert[{x}][{y}]={{"TERRAIN_{terrain}",-1,"CONTINENT_ZEALANDIA",{{{{0,-1}},{{0,-1}},{{0,-1}}}},{{-1,1}},{{0,0,0}},-1}}')
                file.write("\n\n\treturn MapToConvert\nend\n\n")

    except IOError as e:
        print(f"Error processing file {input_file}: {e}")


# Define template and output file paths
file_list = {
    'template/[Author]_[Title].modinfo': os.path.join(output_dir, f"{author}_{title}", f"{author}_{title}.modinfo"),
    'template/[Author]_[Title]_Map.lua': os.path.join(output_dir, f"{author}_{title}/Lua", f"{author}_{title}_Map.lua"),
    'template/Config_Text.xml': os.path.join(output_dir, f"{author}_{title}/Config", "Config_Text.xml"),
    'template/Config.xml': os.path.join(output_dir, f"{author}_{title}/Config", "Config.xml"),
    'template/Map.xml': os.path.join(output_dir, f"{author}_{title}/Map", "Map.xml"),
    'template/MapText.xml': os.path.join(output_dir, f"{author}_{title}/Map", "MapText.xml"),
    'template/ExtraPlacement.xml': os.path.join(output_dir, f"{author}_{title}/Map", "ExtraPlacement.xml"),
    'template/NaturalWonders.xml': os.path.join(output_dir, f"{author}_{title}/Map", "NaturalWonders.xml")
}

# Apply replacements in all template files
replacements = {'[MODID]': mod_id, '[Author]': author, '[Title]': title, '[Length]': str(length),
                '[Height]': str(height)}
for input_file, output_file in file_list.items():
    replace_words(input_file, output_file, replacements)
