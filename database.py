import sqlite3
import ui
from error.artwork_error import ArtworkError
from error.artist_error import ArtistError

db = 'catalog.sqlite'

class SQLCatalogDB():

    def __init__(self):
        with sqlite3.connect(db) as con:
            con.execute('CREATE TABLE IF NOT EXISTS artists (artistid INTEGER PRIMARY KEY, artistname TEXT UNIQUE, artistemail TEXT)')
            con.execute('CREATE TABLE IF NOT EXISTS artworks (artname TEXT UNIQUE, artistname TEXT, availability TEXT, artist INTEGER, FOREIGN KEY(artist) REFERENCES artists(artistid))')
        con.close()


    def add_artist(self, artist, email):

        artistName = artist
        artistEmail = email

        try:
            with sqlite3.connect(db) as con:
                cursor = con.cursor()
                cursor.execute('SELECT * FROM artists WHERE artistname = ?', (artistName,))
                artist_check = cursor.fetchone()
                if artist_check is None:
                    con.execute('INSERT INTO artists VALUES (NULL, ?, ?)', (artistName, artistEmail))
                    print('\nArtist added to database')
                else:
                    print('\nArtist already exists in database')
        except sqlite3.IntegrityError:
            raise ArtistError(f'\nError inserting: cannot not add duplicate artist')
        con.close()


    def add_artwork(self, artwork, artist):

        availability = 'Unavailable'
        
        try:
            with sqlite3.connect(db) as con:
                cursor = con.cursor()
                cursor.execute('SELECT artistid FROM artists WHERE artistname = ?', (artist,))
                artistCheck = cursor.fetchone()
                if artistCheck:
                    idInt = int(artistCheck[0])
                cursor.execute('SELECT * FROM artworks WHERE artname = ?', (artwork,))
                artcheck = cursor.fetchone()

                if artistCheck is None:
                    print('\nNo Artists found by that name - Please add this artist before adding their artwork')
                elif artcheck:
                    print('\nA piece of art by that name is already in the database.')
                else:
                    con.execute('INSERT INTO artworks VALUES (?, ?, ?, ?)', (artwork, artist, availability, idInt))
                    print('\nArtwork added to database')
        except:
            raise ArtworkError('\nError inserting artwork')
        con.close()

    
    def get_artist(self, artistName):

        try:
            with sqlite3.connect(db) as con:
                results = con.execute('SELECT * FROM artists WHERE artistname like ?', (artistName,))
                first_result = results.fetchone()
                if first_result:
                    return first_result
                else:
                    print('\nNo artists found with that name.')
            con.close()
        except:
            raise ArtistError('Error searching for artist ' + artistName)

    
    def get_artwork(self, artwork):

        try:
            with sqlite3.connect(db) as con:
                cursor = con.cursor()
                cursor.execute('SELECT * FROM artworks WHERE artname = ?', (artwork,))
                resultTest = con.execute('SELECT * FROM artworks WHERE artname = ?', (artwork,))
                if cursor.fetchone() is None:
                    print('\nNo artwork found with that name')
                else:
                    for row in resultTest:
                        print('\nArtwork: ' + row[0] + ' | Artist: ' + row[1] + ' | Availability: ' + row[2])
            con.close()
        except:
            raise ArtworkError('\nError searching for artwork')

    def get_artist_artwork(self, artist):

        try:
            with sqlite3.connect(db) as con:
                cursor = con.cursor()
                cursor.execute('SELECT * FROM artworks WHERE artistname = ?', (artist,))
                results = con.execute('SELECT * FROM artworks WHERE artistname = ?', (artist,))
                if cursor.fetchone() is None:
                    print('\nNo artwork found by that artist')
                else:
                    for row in results:
                        print('\nArtist: ' + row[1] + ' | Artwork: ' + row[0] + ' | Availability: ' + row[2])
            con.close()
        except:
            raise ArtworkError('\nError searching for artwork')
    
    
    def change_availability(self, artwork):
        artName = artwork
        available = 'Available'
        unavailable = 'Unavailable'

        try:
            with sqlite3.connect(db) as con:
                cursor = con.cursor()
                results = cursor.execute('SELECT * FROM artworks where artname = ?', (artName,))
                if cursor.fetchone is None:
                    print('No artwork found with that name')
                else:
                    for row in results:
                        if row[2] == 'Unavailable':
                            con.execute('UPDATE artworks SET availability = ? WHERE artname = ?', (available, artName))
                            print('\nArtwork is now available')
                        elif row[2] == 'Available':
                             con.execute('UPDATE artworks SET availability = ? WHERE artname = ?', (unavailable, artName))
                             print('\nArtwork is now unavailable')
                        else:
                            print('\nUnable to update artwork availability')
            con.close()
        except:
            raise ArtworkError('\nError updating artwork availability')


    def get_artwork_available(self, artist):

        available = 'Available'
        
        try:
            with sqlite3.connect(db) as con:
                cursor = con.cursor()
                cursor.execute('SELECT * FROM artworks WHERE artistname like ? AND availability = ?', (artist, available))
                results = con.execute('SELECT * FROM artworks WHERE artistname like ? and availability = ?', (artist, available))
                if cursor.fetchone() is None:
                    print('\nNo available artwork found by that artist')
                else:
                    for row in results:
                        print('\nArtist: ' + row[1] + ' | Artwork: ' + row[0] + ' | Availability: ' + row[2])
            con.close()
        except:
            raise ArtworkError('\nError fetching artwork')

    def get_all_available_artwork(self):

        availability = 'Available'
        try:
            with sqlite3.connect(db) as con:
                cursor = con.cursor()
                resultsCheck = cursor.execute('SELECT * FROM artworks WHERE availability = ?', (availability,))
                results = con.execute('SELECT * FROM artworks WHERE availability = ?', (availability,))
                if resultsCheck.fetchone() is None:
                    print('\nNo artwork available at this time')
                else:
                    for row in results:
                        print('\nArtist: ' + row[1] + ' | Artwork: ' + row[0] + ' | Availability: ' + row[2])
            con.close()
        except:
            raise ArtworkError('\nError fetching artwork')

    
    
    def delete_artwork(self, artwork):

        try:
            with sqlite3.connect(db) as con:
                cursor = con.cursor()
                cursor.execute('SELECT * FROM artworks WHERE artname = ?', (artwork,))
                resultTest = con.execute('SELECT * FROM artworks WHERE artname like ?', (artwork,))
                if cursor.fetchone() is None:
                    print('\nNo artwork found with that name')
                else:
                    for row in resultTest:
                        print('\nArtwork: ' + row[0] + ' | Artist: ' + row[1] + ' | Availability: ' + row[2])
                        userInput = ui.yes_no_input('\nAre you sure you want to delete this artwork? ')
                        if userInput == 'Yes':
                            con.execute('DELETE FROM artworks WHERE artname = ?', (artwork,))
                            print('Artwork deleted from database')
                        else:
                            pass
            con.close()
        except:
            raise ArtworkError('\nError searching for artwork')
