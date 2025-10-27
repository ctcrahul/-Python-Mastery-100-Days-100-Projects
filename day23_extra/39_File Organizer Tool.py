import os
import shutil

def create_folders(base_path):
	folders = ["Documents", "Images", "Videos", "Audio", "Others"]
	for folder in folders:
		folder_path = os.path.join(base_path, folder)
		os.makedirs(folder_path, exist_ok=True)


def move_file(file_path, base_path, folder_name):
	target_folder = os.path.join(base_path, folder_name)
	shutil.move(file_path, target_folder)


def get_folder_for_file(file_name):
	file_extentions = {
		"Documents": [".pdf", ".docx", ".txt", ".xlsx"],
        "Images": [".jpg", ".png", ".gif", ".bmp"],
        "Videos": [".mp4", ".mov", ".avi", ".mkv"],
        "Audio": [".mp3", ".wav", ".flac"],
	}
	for folder, extentions in file_extentions.items():
		if any(file_name.endswith(ext) for ext in extentions):
			return folder
	return "Others"


def organize_files(base_path):
	for file_name in os.listdir(base_path):
		file_path = os.path.join(base_path, file_name)
		if os.path.isfile(file_path):
			folder_name = get_folder_for_file(file_name)
			move_file(file_path, base_path, folder_name)


def main():
	print("Welcome to the File Organizer Tool!")
	base_path = input("Enter the path of the folder to organize: ")
	if not os.path.exists(base_path):
		print("Invalid path. Please Try again.")
		return

	create_folders(base_path)
	organize_files(base_path)
	print("Files have been organized successfully!")

if __name__ == "__main__":
	main()
	














