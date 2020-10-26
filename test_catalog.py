import sqlite3
import unittest
from unittest import TestCase
import database 
from error.artwork_error import ArtworkError
from error.artist_error import ArtistError

class TestCatalogDB(TestCase):

    test_db_url = 'test_catalog.db'

    """
    Before running these test, create test_catalog.db
    Create expected artist/artworks tables
    """

    # The name of this method is important - the test runner will look for it
    def setUp(self):
        database.db = self.test_db_url


        # drop everything from the DB to always start with an empty database
        with sqlite3.connect(self.test_db_url) as con:
            con.execute('DROP TABLE IF EXISTS artists')
            con.execute('DROP TABLE IF EXISTS artworks')
        con.close()

        with sqlite3.connect(self.test_db_url) as con:
            con.execute('CREATE TABLE artists (artistid INTEGER PRIMARY KEY, artistname TEXT UNIQUE, artistemail TEXT)')
            con.execute('CREATE TABLE artworks (artname TEXT UNIQUE, artistname TEXT, availability TEXT, artist INTEGER, FOREIGN KEY(artist) REFERENCES artists(artistid))')
        con.close()

        self.db = database.SQLCatalogDB()
    

    def test_add_new_artist(self):
        artistName = 'Carl'
        artistEmail = 'Carl@gmail.com'
        self.db.add_artist(artistName, artistEmail)
        expected = {1, 'Carl', 'Carl@gmail.com'}
        self.compare_db_to_expected(expected)


    def test_will_not_add_duplicate_artist(self):
        # this test is correct and it's identifying 
        # an error in your code - your add_artist
        # function is not raising an error if duplicate name 
        artistName = 'Carl'
        artistEmail = 'Carl@gmail.com'
        self.db.add_artist(artistName, artistEmail)

        with self.assertRaises(ArtistError):
            artistName = 'Carl'
            artistEmail = 'Carl@gmail.com'
            self.db.add_artist(artistName,artistEmail)


    def test_change_availability(self):
        # arrange....
        self.db.add_artist('bob', 'b@b.com')  
        self.db.add_artwork('Painting', 'bob') # assume it starts as available??

        # action... 
        self.db.change_availability('Painting')

        # assert...
        # TODO find painting in DB and assert it's not available


    def test_delete_artwork(self):
        pass

    def test_add_duplicate_artist(self):
        pass

    def test_add_duplicate_art(self):
        pass

    def test_add_art_fake_artist(self):
        pass



    # This is not a test method, instead, it's used by the test methods
    def compare_db_to_expected(self, expected):

        conn = sqlite3.connect(self.test_db_url)
        all_data = conn.execute('SELECT * FROM artists').fetchall()

        # Same rows in DB as entries in expected dictionary
        self.assertEqual(len(expected.keys()), len(all_data))

        for row in all_data:
            # Artist exists, and email is correct
            print(row)
            self.assertIn(row[0], expected.keys())
            self.assertEqual(expected[row[0]], row[1])

        conn.close()


if __name__ == '__main__':
    unittest.main()