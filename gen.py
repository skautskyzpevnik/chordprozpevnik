#!/usr/bin/env python3
import os
import glob
import logging
import json
from urllib.parse import quote

folder_path_song = 'songs/'
folder_path_no_chords = 'no_chords/'
folder_path_songbooks = 'songbooks/'

final = {}

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

#songs = dict(sorted(songs.items()))

songs = dict(sorted(songs.items(), key=lambda item: item[1]["title"]))

for song in songs:
    print("Extracted: " + songs[song]['title'] + " - " + songs[song]['artist'])

print("Extracted " + str(len(songs)) + " songs.")

final["songbooks"] = []
## extract songbooks


songbook_file_list = glob.glob(os.path.join(folder_path_songbooks, '*'))
for songbook in songbook_file_list:
    with open(songbook, "r") as json_file:
        # Load the JSON data into a Python dictionary
        data = json.load(json_file)
    for song in data["songs"]:
        if not (quote(song["title"]+ "-" + song["artist"]) in songs):
            print("Song from songbook \"" + data["title"] + "\" not in songs: " + song["title"]+ " - " + song["artist"])

    final["songbooks"].append({
        "title": data["title"],
        "subtitle": data["subtitle"],
        "file": songbook
    })

final["songs"] = songs

with open("list.json", 'w', encoding='utf-8') as file:
        json.dump(final, file, indent=4, ensure_ascii=False)