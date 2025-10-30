import os
import shutil
from mutagen import File
import json

def scan_directory(directory, extensions=(".mp3", ".flac", ".wav")):
    music_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(extensions):
                music_files.append(os.path.join(root, file))
    return music_files

def extract_metadata(file_path):
    try:
        audio = File(file_path, easy=True)
        return {
            "title": audio.get("title", ["Unknown Title"])[0],
            "artist": audio.get("artist", ["Unknown Artist"])[0],
            "album": audio.get("album", ["Unknown Album"])[0],
            "genre": audio.get("genre", ["Unknown Genre"])[0]
        }
    except Exception as e:
        print(f"Error extracting metadata for {file_path}: {e}")
        return None

def organize_files(music_files, output_directory):
    for file in music_files:
        metadata = extract_metadata(file)
        if metadata:
            artist = metadata["artist"]
            album = metadata["album"]

            artist_folder = os.path.join(output_directory, artist)
            album_folder = os.path.join(artist_folder, album)

            os.makedirs(album_folder, exist_ok=True)
            destination = os.path.join(album_folder, os.path.basename(file))
            shutil.move(file, destination)
            print(f"Moved: {file} -> {destination}")

def save_summary_to_json(music_files, output_file):
    summary = []
    for file in music_files:
        metadata = extract_metadata(file)
        if metadata:
            summary.append(metadata)

    with open(output_file, "w") as json_file:
        json.dump(summary, json_file, indent=4)
    print(f"Summary saved to {output_file}")

def main():
    print("Welcome to the Music Playlist Organizer!")
    music_directory = input("Enter the path to your music directory: ")
    output_directory = input("Enter the path for the organized music directory: ")

    music_files = scan_directory(music_directory)
    if not music_files:
        print("No music files found.")
        return

    print(f"Found {len(music_files)} music files.")
    save_summary_to_json(music_files, "music_summary.json")
    organize_files(music_files, output_directory)
    print("Music organization complete!")

if __name__ == "__main__":
    main()
