#!/usr/bin/env python3
import os
import glob
import logging
import json

folder_path = 'songs/'

def extract_chordpro_info(file_path):
    title = ""
    artist = ""
    with open(file_path, 'r') as chordpro_file:
        for line in chordpro_file:
            #print(line)
            if line.strip().startswith('{title:'):
                # Extract the title from the line using string manipulation
                title = line.strip().split(':', 1)[1].rstrip('}').strip()
            elif line.strip().startswith('{artist:'):
                artist = line.strip().split(':', 1)[1].rstrip('}').strip()
            if title != "" and artist != "":
                break
    if title == "" and artist == "":
        # If the title is not found, return None or raise an exception as appropriate
        return None
    else:
        return {
            "name": title + " - " + artist,
            "title": title,
            "artist": artist,
            "file": os.path.splitext(os.path.basename(file_path))[0]
        }
        

# List all files in the folder with a specific pattern, e.g., all files ending with .txt
file_list = glob.glob(os.path.join(folder_path, '*.chordpro'))

songs = {}
for file in file_list:
    info = extract_chordpro_info(file)
    if info is None:
        logging.warning("Unable to extract info from file '" + file + "'\n skipping")
        continue
    songs[info["name"]] = {"title": info["title"], "artist": info["artist"], "file": info["file"]}

alphabeth = {}

for key, value in songs.items():
    first_char = key[0]
    if first_char in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        first_char = "0-9"
    if first_char not in alphabeth:
        alphabeth[first_char] = {}
    if key not in alphabeth[first_char]:
        alphabeth[first_char][key] = {}
    alphabeth[first_char][key] = value

for key in alphabeth:
    with open(key + ".json", 'w', encoding='utf-8') as file:
        json.dump(alphabeth[key], file, indent=4, ensure_ascii=False)

with open("list.json", 'w', encoding='utf-8') as file:
        json.dump(list(alphabeth.keys()), file, indent=4, ensure_ascii=False)