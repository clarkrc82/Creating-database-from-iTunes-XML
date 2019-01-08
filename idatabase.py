import xml.etree.ElementTree as ET
import sqlite3

# Creates and connects to db
conn = sqlite3.connect('iTunes.sqlite')
cur = conn.cursor()

# Makes new tables in db
cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;
DROP TABLE IF EXISTS Genre;

CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name  TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name  TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    album   TEXT UNIQUE,
    year  INTEGER
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    song TEXT,
    album_id  INTEGER,
    genre_id  INTEGER,
    length INTEGER, 
    count INTEGER,
    rating INTEGER
    
);
''')

# Function that finds the value in key and returns its text
# If value in key is blank, returns 'Unkown' as value
def lookup(i, key):
    found = False
    for child in i:
        if found : return child.text
        if child.tag == 'key' and child.text == key:
            found = True
    return 'Unkown'

doc = 'iTunes.xml'
library = ET.parse(doc)
songs = library.findall('dict/dict/dict') #Songs are in the 2nd child dict
# Variable for song count
song_count = 0

# Loops through and enters into db all songs in doc
for entry in songs:
    # Uses the lookup function to return the text from key
    name = lookup(entry, 'Name')
    artist = lookup(entry, 'Artist')
    album = lookup(entry, 'Album')
    genre = lookup(entry, 'Genre')
    length = lookup(entry, 'Total Time')
    year = lookup(entry, 'Year')
    count = lookup(entry, 'Play Count')
    rating = lookup(entry, 'Rating')
    
    # Optional print msg
    #print(name, artist, album, genre, length, year, rating, count)
    
    # Inserts new Artist into db. If Artist in already in db, it ignores it and moves on.
    cur.execute('''INSERT OR IGNORE INTO Artist (name) 
        VALUES ( ? )''', ( artist, ) )
    cur.execute('SELECT id FROM Artist WHERE name = ? ', (artist, ))
    # This essentialy creates the unique artist_id
    artist_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Album (album, artist_id, year) 
        VALUES ( ?, ?, ? )''', ( album, artist_id, year ) )
    cur.execute('SELECT id FROM Album WHERE album = ? ', (album, ))
    album_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Genre (name) 
        VALUES ( ? )''', (genre, ))
    cur.execute('SELECT id FROM Genre WHERE name = ? ', (genre, ))
    genre_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Track
        (song, album_id, genre_id, length, count, rating ) 
        VALUES ( ?, ?, ?, ?, ?, ? )''', 
        (name, album_id, genre_id, length, count, rating))
    song_count += 1
    conn.commit()
# Prints out how many songs found compaired to songs entered into db
print('Found {} songs in {}.'.format((len(songs)), doc))
print('{} songs entered into the database.'.format(song_count))
