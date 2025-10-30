"                                                   Day: 42
                                
                                           Music Playlist Organizer
                                 
"

import os
import shutil
import logging
from mutagen import File
import json
import hashlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# Configure logging
logging.basicConfig(filename='music_organizer.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def scan_directory(directory, extensions=(".mp3", ".flac", ".wav")):
    music_files = []
    directory = Path(directory)  # Using pathlib for easier path handling
    for file in directory.rglob("*"):
        if file.suffix.lower() in extensions:
            music_files.append(file)
    return music_files

def extract_metadata(file_path):
    try:
        audio = File(file_path, easy=True)
        metadata = {
            "title": audio.get("title", ["Unknown Title"])[0],
            "artist": audio.get("artist", ["Unknown Artist"])[0],
            "album": audio.get("album", ["Unknown Album"])[0],
            "genre": audio.get("genre", ["Unknown Genre"])[0],
            "year": audio.get("year", ["Unknown Year"])[0] if audio.get("year") else "Unknown Year",
            "track": audio.get("tracknumber", ["Unknown Track"])[0]
        }
        return metadata
    except Exception as e:
        logging.error(f"Error extracting metadata for {file_path}: {e}")
        return None

def generate_file_hash(file_path):
    """Generate MD5 hash for duplicate file detection."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def organize_files(music_files, output_directory, existing_hashes=set()):
    for file in music_files:
        metadata = extract_metadata(file)
        if metadata:
            artist = metadata["artist"]
            album = metadata["album"]

            artist_folder = os.path.join(output_directory, artist)
            album_folder = os.path.join(artist_folder, album)

            os.makedirs(album_folder, exist_ok=True)
            destination = os.path.join(album_folder, file.name)

            # Check for duplicate based on file hash
            file_hash = generate_file_hash(file)
            if file_hash in existing_hashes:
                logging.info(f"Duplicate file skipped: {file}")
                continue

            existing_hashes.add(file_hash)
            shutil.move(file, destination)
            logging.info(f"Moved: {file} -> {destination}")

def save_summary_to_json(music_files, output_file):
    summary = []
    for file in music_files:
        metadata = extract_metadata(file)
        if metadata:
            summary.append(metadata)

    with open(output_file, "w") as json_file:
        json.dump(summary, json_file, indent=4)
    logging.info(f"Summary saved to {output_file}")

def main():
    print("Welcome to the Music Playlist Organizer!")
    music_directory = input("Enter the path to your music directory: ")
    output_directory = input("Enter the path for the organized music directory: ")

    music_files = scan_directory(music_directory)
    if not music_files:
        print("No music files found.")
        logging.warning("No music files found in the provided directory.")
        return

    print(f"Found {len(music_files)} music files.")
    save_summary_to_json(music_files, "music_summary.json")

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor() as executor:
        executor.submit(organize_files, music_files, output_directory, set())

    print("Music organization complete!")

if __name__ == "__main__":
    main()


############################################################################################################################################################################
                                                             Use this code and support us
############################################################################################################################################################################




        executor.submit(organize_files, music_files, output_directory, set())

    print("Music organization complete!")

if __name__ == "__main__":
    main()


def main():
    print("Welcome to the Music Playlist Organizer!")
    music_directory = input("Enter the path to your music directory: ")
    output_directory = input("Enter the path for the organized music directory: ")


    print(f"Found {len(music_files)} music files.")
    save_summary_to_json(music_files, "music_summary.json")

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor() as executor:
      
def save_summary_to_json(music_files, output_file):
    summary = []
    for file in music_files:
        metadata = extract_metadata(file)
        if metadata:
            summary.append(metadata)

    with open(output_file, "w") as json_file:
        json.dump(summary, json_file, indent=4)
    logging.info(f"Summary saved to {output_file}")


            # Check for duplicate based on file hash


            artist_folder = os.path.join(output_directory, artist)
            album_folder = os.path.join(artist_folder, album)

            os.makedirs(album_folder, exist_ok=True)
            destination = os.path.join(album_folder, file.name)

            file_hash = generate_file_hash(file)
            if file_hash in existing_hashes:
                logging.info(f"Duplicate file skipped: {file}")
                continue



    music_files = scan_directory(music_directory)
            existing_hashes.add(file_hash)
            shutil.move(file, destination)
            logging.info(f"Moved: {file} -> {destination}")

    if not music_files:
        print("No music files found.")
        logging.warning("No music files found in the provided directory.")
        return
