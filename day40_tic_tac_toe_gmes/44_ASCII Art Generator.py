from PIL import Image

def load_image(image_path, new_width=100):
	# Open Image
	img = Image.open(image_path)
	#Calculate Aspect Ratio
	aspect_ratio = img.height / img.width
	new_height = int(new_width * aspect_ratio * 0.55)
	img = img.resize((new_width, new_height))
	return img

def convert_to_grayscale(img):
	return img.convert("L")

def map_pixels_to_ascii(img):
	ascii_chars = "@%#*+=-:. "
	pixels = img.getdata()
	ascii_str = "".join([ascii_chars[pixel // 25] for pixel in pixels])
	return ascii_str

def generate_ascii_art(image_path, new_width=100):
	#Load and resize image
	img = load_image(image_path, new_width)
	#Convert to Grayscale
	gray_image = convert_to_grayscale(img)
	# Map Pixels to Ascii
	ascii_str = map_pixels_to_ascii(gray_image)
	# Format ASCII String into Rows
	ascii_art = "\n".join([ascii_str[i:i + new_width] for i in range(0, len(ascii_str), new_width)])
	return ascii_art

def save_ascii_art(ascii_art, output_path):
	with open(output_path, "w") as file:
		file.write(ascii_art)

def main():
    print("Welcome to the ASCII Art Generator!")
    image_path = input("Enter the path to your image: ")
    output_path = input("Enter the path to save the ASCII art (e.g., output.txt): ")
    new_width = int(input("Enter the desired width of the ASCII art (default is 100): ") or 100)
    
    try:
        ascii_art = generate_ascii_art(image_path, new_width)
        save_ascii_art(ascii_art, output_path)
        print(f"ASCII art generated and saved to {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()














