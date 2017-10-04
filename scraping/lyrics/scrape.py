import pylyrics3
import string

artist = 'bon iver'
file = artist.replace(" ", "_")
file2 = artist.replace(" ", "_") + "_stripped"
lyrics = pylyrics3.get_artist_lyrics(artist)


def scrape(outputfile):
    with open(outputfile, 'w') as db:
        for x in lyrics:
            db.write(lyrics[x])


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

scrape(file)
remove_dupes(file, file2)

