import ui 
import database

catalog_db = database.SQLCatalogDB()


def main():
    
    while True:
    # what does the user want to do?
    # print menu
        task = input('\nPlease enter the number corresponding to the action you would like to perform: \n1 - Add Artist \n2 - Add Artwork \n3 - Search Artworks \n4 - See All of an Artists\' Artworks \n5 - Search for an Artists\' Available Artworks \n6 - See All Available Artwork \n7 - Change an Artwork\'s Availability \n8 - Delete an Artwork \nEnter Option: ') 

        if task == '1':
            add_artist()
        elif task == '2':
            add_artwork()
        elif task == '3':
            search_artwork()
        elif task == '4':
            search_artist_artwork()
        elif task == '5':
            search_artist_available_artwork()
        elif task == '6':
            view_all_available_artwork()
        elif task == '7':
            change_artwork_availability()
        elif task == '8':
            delete_artwork()
        else:
            print('\nPlease enter a valid menu option.\n')


def add_artist():
    # get input 
    name = ui.get_non_empty_string('\nWhat is the Artists\' name? ')
    email = ui.get_non_empty_string('What is the Artists\' email? ')
    catalog_db.add_artist(name, email)

def add_artwork():
    artName = ui.get_non_empty_string('\nWhat is the name of the artwork? ')
    artistName = ui.get_non_empty_string('Who created this artwork? ')
    catalog_db.add_artwork(artName, artistName)

def search_artwork():
    artName = ui.get_non_empty_string('\nEnter the name of the artwork to search for: ')
    catalog_db.get_artwork(artName)

def search_artist_artwork():
    artistName = ui.get_non_empty_string('\nEnter the name of the artist to search for: ')
    catalog_db.get_artist_artwork(artistName)

def search_artist_available_artwork():
    artistName = ui.get_non_empty_string('\nEnter the name of the artist to get available artwork for: ')
    catalog_db.get_artwork_available(artistName)

def change_artwork_availability():
    artName = ui.get_non_empty_string('\nEnter the name of the artwork to change the availability of: ')
    catalog_db.change_availability(artName)

def view_all_available_artwork():
    catalog_db.get_all_available_artwork()

def delete_artwork():
    artName = ui.get_non_empty_string('\nEnter the name of the artwork to delete: ')
    catalog_db.delete_artwork(artName)


if __name__ == '__main__':
    main()

