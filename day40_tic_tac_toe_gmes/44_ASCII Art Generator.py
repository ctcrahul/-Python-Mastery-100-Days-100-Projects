"""                                                             Day 44
          
                                                         ASCII Art Generator                                                          
"""

import os
import numpy as np
from PIL import Image, ImageEnhance
from concurrent.futures import ThreadPoolExecutor

def load_image(image_path, new_width=100):
    try:
        img = Image.open(image_path)
    except IOError:
        raise ValueError(f"Error: Cannot open image {image_path}. Please check the file path or format.")

    # Calculate Aspect Ratio
    aspect_ratio = img.height / img.width
    new_height = int(new_width * aspect_ratio)
    img = img.resize((new_width, new_height))
    return img

def enhance_image(img, brightness=1.0, contrast=1.0, sharpen=1.0):
    # Enhance Brightness
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(brightness)
    
    # Enhance Contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(contrast)
    
    # Sharpen Image
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(sharpen)
    
    return img

def convert_to_grayscale(img):
    return img.convert("L")

def map_pixels_to_ascii(img, ascii_chars="@%#*+=-:. "):
    pixels = np.array(img)
    ascii_str = "".join([ascii_chars[pixel // 25] for pixel in pixels.flatten()])
    return ascii_str

def generate_ascii_art(image_path, new_width=100, brightness=1.0, contrast=1.0, sharpen=1.0, ascii_chars="@%#*+=-:. "):
    try:
        img = load_image(image_path, new_width)
        img = enhance_image(img, brightness, contrast, sharpen)
        gray_image = convert_to_grayscale(img)
        ascii_str = map_pixels_to_ascii(gray_image, ascii_chars)

        # Format ASCII String into Rows
        ascii_art = "\n".join([ascii_str[i:i + new_width] for i in range(0, len(ascii_str), new_width)])
        return ascii_art
    except Exception as e:
        raise ValueError(f"An error occurred during ASCII art generation: {e}")

def save_ascii_art(ascii_art, output_path, append=False):
    mode = "a" if append else "w"
    try:
        with open(output_path, mode) as file:
            file.write(ascii_art)
            file.write("\n")
    except IOError:
        raise ValueError(f"Error: Unable to save the ASCII art to {output_path}. Please check file permissions.")

def process_image_in_parallel(image_path, new_width=100, brightness=1.0, contrast=1.0, sharpen=1.0, ascii_chars="@%#*+=-:. "):
    try:
        ascii_art = generate_ascii_art(image_path, new_width, brightness, contrast, sharpen, ascii_chars)
        return ascii_art
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    print("Welcome to the Advanced ASCII Art Generator!")
    
    # User Inputs with defaults and validations
    image_path = input("Enter the path to your image: ").strip()
    if not os.path.isfile(image_path):
        print(f"Error: {image_path} is not a valid file path!")
        return

    output_path = input("Enter the path to save the ASCII art (e.g., output.txt): ").strip()
    if not os.path.isdir(os.path.dirname(output_path)):
        print(f"Error: Invalid directory for output file!")
        return
    
    try:
        new_width = int(input("Enter the desired width of the ASCII art (default is 100): ") or 100)
        if new_width <= 0:
            raise ValueError("Width must be a positive integer.")
    except ValueError as e:
        print(f"Invalid input: {e}")
        return
    
    brightness = float(input("Enter brightness level (default is 1.0, range 0.0 to 2.0): ") or 1.0)
    contrast = float(input("Enter contrast level (default is 1.0, range 0.0 to 2.0): ") or 1.0)
    sharpen = float(input("Enter sharpness level (default is 1.0, range 0.0 to 2.0): ") or 1.0)
    
    custom_ascii = input("Would you like to provide your custom ASCII characters? (y/n): ").strip().lower()
    if custom_ascii == "y":
        ascii_chars = input("Enter custom ASCII characters in order of darkness (e.g. @%#*+=-:.): ").strip()
    else:
        ascii_chars = "@%#*+=-:. "
    
    # Process Image and Generate ASCII Art
    ascii_art = process_image_in_parallel(image_path, new_width, brightness, contrast, sharpen, ascii_chars)

    if ascii_art:
        print(f"\nASCII art generated successfully!\n")
        print(ascii_art)

        save_option = input("Do you want to save the ASCII art to a file? (y/n): ").strip().lower()
        if save_option == "y":
            append_option = input("Do you want to append to the file if it exists? (y/n): ").strip().lower() == "y"
            save_ascii_art(ascii_art, output_path, append=append_option)
            print(f"ASCII art saved to {output_path}")
    else:
        print("Failed to generate ASCII art.")

if __name__ == "__main__":
    main()









#############################################################################################################################################################################
                                                        Thanks for visting and keep support us
#############################################################################################################################################################################




        save_option = input("Do you want to save the ASCII art to a file? (y/n): ").strip().lower()
        if save_option == "y":
            append_option = input("Do you want to append to the file if it exists? (y/n): ").strip().lower() == "y"
            save_ascii_art(ascii_art, output_path, append=append_option)
            print(f"ASCII art saved to {output_path}")


    else:
                      ascii_chars = "@%#*+=-:. "        return
    
    brightness = float(input("Enter brightness level (default is 1.0, range 0.0 to 2.0): ") or 1.0)
    contrast = float(input("Enter contrast level (default is 1.0, range 0.0 to 2.0): ") or 1.0)
    sharpen = float(input("Enter sharpness level (default is 1.0, range 0.0 to 2.0): ") or 1.0)
    
    custom_ascii = input("Would you like to provide your custom ASCII characters? (y/n): ").strip().lower()
    if custom_ascii == "y":
        ascii_chars = input("Enter custom ASCII characters in order of darkness (e.g. @%#*+=-:.): ").strip()
    else:
    
    # Process Image and Generate ASCII Art
    ascii_art = process_image_in_parallel(image_path, new_width, brightness, contrast, sharpen, ascii_chars)

    if ascii_art:    try:
        new_width = int(input("Enter the desired width of the ASCII art (default is 100): ") or 100)
        if new_width <= 0:
            raise ValueError("Width must be a positive integer.")
    except ValueError as e:
        print(f"Invalid input: {e}")
        print(f"\nASCII art generated successfully!\n")
        print(ascii_art)

        print("Failed to generate ASCII art.")

if __name__ == "__main__":
    main()


C:\\Users\\rahul\\OneDrive\\Pictures\\Screenshots\\rahuu.png
