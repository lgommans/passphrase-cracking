import pylyrics3
import string
from pathlib import Path
import os

# Retrieves lyrics from a particular artist and writes it to a file

def get_lyrics(artist):
    try:
        filename = artist.replace(" ", "_")  # No spaces in filename
        if "/" in filename:  # Prevent making another directory for names such as AC/DC
            filename = filename.replace("/", "-")
        if Path('database/'+filename).exists():  # Prevent double work (remove a file if you want to rebuild its DB)
            print("Database for " + filename + " is already there.")
        else:
            print("Writing database for " + filename)
            with open('database/' + filename, 'w') as file:
                lyrics = pylyrics3.get_artist_lyrics(artist)
                for x in lyrics:
                    file.write(lyrics[x])  # Write all lyrics to file
    except Exception as error:
        print(artist + " threw an exception")
        print(error)


# Read in an artisfile and call get_lyrics for each artist

def scrape(artistfile):
    artists = open(artistfile, 'r')
    for artist in artists:
        artist = artist.strip()
        get_lyrics(artist)
    artists.close()


# remove duplicate lines an punctuation

def remove_dupes(inputfile, outputfile):
    lines_seen = set() # holds lines already seen
    outfile = open(outputfile, "a")
    remove = dict.fromkeys(map(ord, string.punctuation)) # remove punctuation
    for line in open(inputfile, "r"):
        if line not in lines_seen: # not a duplicate
            outfile.write(line.translate(remove))
            lines_seen.add(line)
    outfile.close()


# Calls remove_dupes for all files in a directory

def strip_files(directory):
    directory = os.fsencode(directory)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        remove_dupes(directory + filename, directory + filename + '.stripped')
