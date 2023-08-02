#!/usr/bin/env python3
import os
import glob
import logging
import json
from urllib.parse import quote

folder_path_song = 'songs/'
folder_path_no_chords = 'no_chords/'

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
            "name": quote(title + "-" + artist),
            "title": title,
            "artist": artist,
            "file": quote(os.path.splitext(file_path)[0])
        }
        

# List all files in the folder with a specific pattern, e.g., all files ending with .txt
file_list = glob.glob(os.path.join(folder_path_no_chords, '*.chordpro'))
file_list.extend(glob.glob(os.path.join(folder_path_song, '*.chordpro')))

songs = {}
for file in file_list:
    info = extract_chordpro_info(file)
    if info is None:
        logging.warning("Unable to extract info from file '" + file + "'\n skipping")
        continue
    songs[info["name"]] = {"title": info["title"], "artist": info["artist"], "file": info["file"]}

for song in songs:
    print("Extracted: " + songs[song]['title'] + " - " + songs[song]['artist'])

with open("list.json", 'w', encoding='utf-8') as file:
        json.dump(songs, file, indent=4, ensure_ascii=False)