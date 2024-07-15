import os
import random
import string
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageDraw
import math
import statistics

# Constants
RGB_LIST = [
    (32, 192, 64), (192, 224, 0),
    (224, 128, 0), (192, 220, 192),
    (255, 255, 255), (64, 64, 192)
]

TERRAIN_DICT = {
    (32, 192, 64): "GRASS",
    (192, 224, 0): "PLAINS",
    (224, 128, 0): "DESERT",
    (192, 220, 192): "TUNDRA",
    (255, 255, 255): "SNOW",
    (0, 160, 192): "COAST",
    (64, 64, 192): "OCEAN"
}

terrain_counts = {
    "GRASS": 0,
    "PLAINS": 0,
    "DESERT": 0,
    "TUNDRA": 0,
    "SNOW": 0,
    "COAST": 0,
    "OCEAN": 0
}

# Utility functions
def get_user_input(prompt, input_type=int, min_value=1):
    """Prompt the user for input."""
    while True:
        try:
            value = input_type(simpledialog.askstring("Input", prompt))
            if value >= min_value:
                return value
            else:
                messagebox.showerror("Invalid Input", f"Please enter a value greater than or equal to {min_value}.")
        except ValueError:
            messagebox.showerror("Invalid Input", f"Invalid input. Please enter a valid {input_type.__name__}.")

def calculate_distance(rgb1, rgb2):
    """Calculate the distance between two RGB values."""
    return math.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(rgb1, rgb2)))

def is_even(value):
    """Do I need to explain..."""
    return 5 if (value % 2) else 8

def different_color_check(x, y, color_corrected_map, map_length, map_height):
    """Check if a pixel is a different color from its neighbors."""
    neighbors = [
        (x - 1, y), (x + 1, y),
        (x, y - 1), (x, y + 1),
        (x + 1, y + 1), (x + 1, y - 1),
        (x - 1, y + 1), (x - 1, y - 1)
    ]

    current_color = color_corrected_map.getpixel((x, y))
    if current_color == (64, 64, 192):
        for nx, ny in neighbors:
            if 0 <= nx < map_length and 0 <= ny < map_height:
                neighbor_color = color_corrected_map.getpixel((nx, ny))
                if neighbor_color != current_color and neighbor_color != (0, 160, 192):
                    return True
    return False

def process_image(image_path, map_length, map_height, output_dir):
    """Process the image and create the color-corrected map."""
    image = Image.open(image_path)
    resized_image = image.resize((map_length, map_height))

    color_corrected_map = Image.new('RGB', (map_length, map_height))
    draw = ImageDraw.Draw(color_corrected_map)

    for x in range(map_length):
        for y in range(map_height):
            pix = resized_image.getpixel((x, y))[:3]
            closest_rgb = min(RGB_LIST, key=lambda rgb: calculate_distance(pix, rgb))
            draw.point((x, y), fill=closest_rgb)

    for y in range(map_height):
        for x in range(map_length):
            if different_color_check(x, y, color_corrected_map, map_length, map_height):
                draw.point((x, y), (0, 160, 192))

    color_corrected_map_path = os.path.join(output_dir, "color_corrected_map.bmp")
    color_corrected_map.save(color_corrected_map_path)

    return color_corrected_map_path

def generate_mod_id(length=32):
    """Generate a random mod ID."""
    characters = string.ascii_lowercase + string.digits
    random_id = ''.join(random.choices(characters, k=length))
    return f"{random_id[:8]}-{random_id[8:12]}-{random_id[12:16]}-{random_id[16:20]}-{random_id[20:]}"

def get_pix(x, y, image):
    """Get the terrain type based on the pixel's RGB value."""
    rgb = image.getpixel((x, y))
    terrain = TERRAIN_DICT.get(rgb, "UNKNOWN")
    terrain_counts[terrain] += 1
    return terrain

def replace_words(input_file, output_file, replacements, image, height, length):
    """Create files"""
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
                for x in range(length):
                    for y in range(height):
                        terrain = get_pix(x, (height-1)-y, image)
                        file.write(
                            f'\nMapToConvert[{x}][{y}]={{"TERRAIN_{terrain}",-1,"CONTINENT_ZEALANDIA",{{{{0,-1}},{{0,-1}},{{0,-1}}}},{{-1,1}},{{0,0,0}},-1}}')
                file.write("\n\n\treturn MapToConvert\nend\n\n")

    except IOError as e:
        print(f"Error processing file {input_file}: {e}")

def create_output_folders(output_dir, author, title):
    """Create folders."""
    folders = [os.path.join(output_dir, f"{author}_{title}/{sub_folder}") for sub_folder in ['Config', 'Lua', 'Map']]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
    return folders

def make_files(output_dir, color_corrected_map_path):
    """Generate and save the output files."""
    try:
        image = Image.open(color_corrected_map_path)
    except IOError as e:
        print(f"Error opening image: {e}")
        exit(1)

    title = simpledialog.askstring("Map Name", "Give your map a name:")
    author = simpledialog.askstring("Author Name", "Enter your username or the name you want to be attributed to your map:")
    length, height = image.size

    mod_id = generate_mod_id()

    create_output_folders(output_dir, author, title)

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

    replacements = {'[MODID]': mod_id, '[Author]': author, '[Title]': title, '[Length]': str(length), '[Height]': str(height)}

    for input_file, output_file in file_list.items():
        replace_words(input_file, output_file, replacements, image, height, length)

def get_percentages(terrain_counts, map_length, map_height):
    image_size = map_length*map_height
    terrain_percentages = {
        "GRASS": (terrain_counts["GRASS"]/image_size)*100,
        "PLAINS": (terrain_counts["PLAINS"]/image_size)*100,
        "DESERT": (terrain_counts["DESERT"]/image_size)*100,
        "TUNDRA": (terrain_counts["TUNDRA"]/image_size)*100,
        "SNOW": (terrain_counts["SNOW"]/image_size)*100,
        "COAST": (terrain_counts["COAST"]/image_size)*100,
        "OCEAN": (terrain_counts["OCEAN"]/image_size)*100
    }
    return terrain_percentages

def grade_map(terrain_percentages):
    grass_plains = terrain_percentages["GRASS"] + terrain_percentages["PLAINS"]
    coast_ocean = terrain_percentages["COAST"] + terrain_percentages["OCEAN"]
    desert_tundra_snow = terrain_percentages["DESERT"] + terrain_percentages["TUNDRA"] + terrain_percentages["SNOW"]

    grass_plains_target = 20
    coast_ocean_target = 70
    desert_tundra_snow_target = 10

    grass_plains_diff = abs(grass_plains - grass_plains_target)
    coast_ocean_diff = abs(coast_ocean - coast_ocean_target)
    desert_tundra_snow_diff = abs(desert_tundra_snow - desert_tundra_snow_target)

    max_diff = 100
    grass_plains_score = max(0, (max_diff - grass_plains_diff))
    coast_ocean_score = max(0, (max_diff - coast_ocean_diff))
    desert_tundra_snow_score = max(0, (max_diff - desert_tundra_snow_diff))

    total_score = grass_plains_score + coast_ocean_score + desert_tundra_snow_score
    normalized_score = total_score / 3


    with open('log.txt', "w") as log:
        log.write(f"SAVANNA: {grass_plains_diff}\n")
        log.write(f"MARINE: {coast_ocean_diff}\n")
        log.write(f"WILDERNESS: {desert_tundra_snow_diff}\n")
        log.write(f"\nTOTAL SCORE: {normalized_score}\n")

def main():
    """Main function to do everything."""
    root = tk.Tk()
    root.withdraw()

    image_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")]
    )

    if not image_path:
        messagebox.showinfo("No file selected", "No file selected, exiting.")
        return

    map_length = get_user_input('Please type the length of the map: ')
    map_height = get_user_input('Please type the height of the map: ')

    output_dir = filedialog.askdirectory(title="Select Output Directory")

    if not output_dir:
        messagebox.showinfo("No directory selected", "No directory selected, exiting.")
        return

    color_corrected_map_path = process_image(image_path, map_length, map_height, output_dir)
    make_files(output_dir, color_corrected_map_path)

    terrain_percentages = get_percentages(terrain_counts, map_length, map_height)
    grade_map(terrain_percentages)

    messagebox.showinfo("Process Completed", "Image processing completed. The files have been saved.")
    print(terrain_counts, map_length, map_height)

if __name__ == "__main__":
    main()
