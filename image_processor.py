import os
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import math

def get_user_input(prompt, input_type=int, min_value=1):
    """Prompt the user for input and validate it."""
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
    return sum((c1 - c2) ** 2 for c1, c2 in zip(rgb1, rgb2)) ** 0.5

def is_even(x_value):
    """Return 8 if x_value is even, otherwise return 5."""
    return 5 if (x_value % 2) else 8

def different_color_check(x, y, color_corrected_map, map_length, map_height):
    """Check if pixel is different color from its neighbors."""
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
    """Processioning."""
    image = Image.open(image_path)
    resized_image = image.resize((map_length, map_height))

    rgb_list = [
        (32, 192, 64), (192, 224, 0),
        (224, 128, 0), (192, 220, 192),
        (255, 255, 255), (64, 64, 192)
    ]

    color_corrected_map = Image.new('RGB', (map_length, map_height))
    draw = ImageDraw.Draw(color_corrected_map)

    for x in range(map_length):
        for y in range(map_height):
            pix = resized_image.getpixel((x, y))[:3]
            closest_rgb = min(rgb_list, key=lambda rgb: calculate_distance(pix, rgb))
            draw.point((x, y), fill=closest_rgb)

    for y in range(map_height):
        for x in range(map_length):
            if different_color_check(x, y, color_corrected_map, map_length, map_height):
                draw.point((x, y), (0, 160, 192))

    color_corrected_map_path = os.path.join(output_dir, "color_corrected_map.bmp")
    color_corrected_map.save(color_corrected_map_path)

    new_length = map_length * 6 + 4
    new_height = map_height * 5 + 3
    output_image = Image.new('RGB', (new_length, new_height), 'white')
    draw = ImageDraw.Draw(output_image)

    y_value = 5

    for y in range(map_height):
        pixel = is_even(y)
        for x in range(map_length):
            landscape = color_corrected_map.getpixel((x, y))[:3]
            draw.point((pixel, y_value), landscape)
            pixel += 6
        y_value += 5

    output_image_path = os.path.join(output_dir, "IMPORT_INTO_YnABMC.bmp")
    output_image.save(output_image_path)

def main():
    """Main function to run everything."""
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

    output_dir = filedialog.askdirectory(
        title="Select Output Directory"
    )

    if not output_dir:
        messagebox.showinfo("No directory selected", "No directory selected, exiting.")
        return

    process_image(image_path, map_length, map_height, output_dir)
    messagebox.showinfo("Process Completed", "Image processing completed. The files have been saved.")

if __name__ == "__main__":
    main()
