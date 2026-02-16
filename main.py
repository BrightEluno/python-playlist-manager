import time
import sys
from models.user import User
from models.song import Song
from service.authentication_service import  AuthenticationService
from service.playlist_service import PlaylistService

VALID_USERNAME = "user123"
VALID_PASSWORD = "Givemetheykey123"

def input_not_empty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This input cannot be empty.")

def show_menu():
    print("\nOptions Available:")
    print("1. Add a song to playlist")
    print("2. Change song details in a playlist")
    print("3. Rename a playlist")
    print("4. Remove a playlist")
    print("5. Remove a song from a playlist")
    print("6. Identify duplicated songs across playlists")
    print("7. Sort playlists by name")
    print("8. Sort songs in each playlist by name ")
    print("9. Shuffle songs in a playlist")
    print("10. Export playlists to file")
    print("11. Load playlists from sample file")
    print("12. Show playlists summary")
    print("0. Logout")
    


def main():
    user  = User(userName=VALID_USERNAME, password=VALID_PASSWORD)
    auth = AuthenticationService(users=user)

    # user Authentication loop
    while True:
        if auth.locked():
            remaining = int((auth.locked_time - time.time()) // 60 ) + 1
            print(f"Too many failed attempts. your account has been locked for {auth.minutes_lock} minutes try again later.")
            sys.exit(1)

        userName = input("Username: ").strip()
        password = input("Password: ").strip()
        if auth.login_attempt(userName, password):
            print("Login Successful\n")
            break
        else:
            attempts_left = auth.max_attempt - auth.failed_attempts
            if auth.locked():
                print(f"Too many failed attempts. your account has been locked for {auth.minutes_lock} minutes.")
                sys.exit(1)
            print(f"Login failed. Attempts left: { attempts_left}")

    svc = PlaylistService()

    """ This is th mean application loop it keeps running until the user choose to exit the application """


    while True:
        #Show the menu options
        show_menu()
        choice = input("Enter your option: ").strip()

        # this exit the application
        if choice == "0":
            print("Goodbye!")
            break

        # the option 1 adding a song to a playlist it creates a playlist if the playlist name dose not exists
        if choice == "1":
            playlist_name = input_not_empty("Playlist name: ")
            name = input_not_empty("Song name: ")
            singer = input_not_empty("Singer name: ")
            genre = input_not_empty( "Genre: " )
            svc.add_song_to_playlist(playlist_name, Song(name=name, singer=singer, genre=genre))
            print(f"Added '{name}' to playlist '{playlist_name}'")

        # Option 2: Editing an existing song in the playlist

        elif choice =="2":
            playlist_name = input_not_empty("Playlist name: ")
            song_name = input_not_empty("Existing song name: ")
            singer = input("Singer (optional): ").strip() or None
            
            # Retrieve the playlist
            p = svc.playlists.get(playlist_name)
            if not p:
                print("Playlist is not found")
                continue

            #Finding song in the playlist 
            s = p.find_song(song_name, singer)
            if not s: 
                print("Song not find in]the playlist ")
                continue

        
            # Collect the updated song details (optional)
            new_name = input("Song new name (keep blank to keep name): ").strip() or None
            new_singer = input("New singer  (keep blank to keep singer name): ").strip() or None
            new_genre = input("New genre name  (keep blank to keep genre name): ").strip() or None

            #update the song details
            s.update(name=new_name, singer=new_singer, genre=new_genre)
            print("Song details updated")

        # Option 3 renaming a playlist
        elif choice == "3":
            old = input_not_empty("Current playlist name: ")
            new = input_not_empty("New playlist name: ")

            try: 
                ok = svc.rename_playlist(old, new)
                if ok:
                    print("Playlist renamed")
                else:
                    print("Playlist not found")
            except ValueError as e:
                print(e)


        #Option 4 delete a playlist
        elif choice == "4":
            playlist_name = input_not_empty("Playlist name to remove: ")
            if svc.delete_playlist(playlist_name):
                print("Playlist removed")
            else:
                print("Playlist not found")

        
        #Option 5 removing a song from a playlist 
        elif choice == "5":
            playlist_name = input_not_empty("Playlist name: ")
            song_name = input_not_empty("Song name to remove: ")
            singer = input("Singer (optional): ").strip() or None
            
            if svc.remove_song_from_playlist(playlist_name, song_name, singer):
                print("song remove")
            else:
                print("song or playlist not found.")
        
        # Option 6 finding duplicated songs across all playlists
        elif choice == "6":
            duplicate = svc.find_duplicates()
            if duplicate: 
                print("playlist containing  duplicated songs: ")
                for d in duplicate: 
                    print(f"- {d}") 
            else:
                print("No duplicated songs across playlists found")
                

        #Option 7 display playlist sorted in alphabetically other
        elif choice == "7":
            sorted_ps = svc.sort_by_name()
            print("Playlist (A to Z):")
            for p in sorted_ps:
                print(f"- {p}")

        
        #Option 8 sorting songs in all playlist by name 

        elif choice == "8":
            for p in svc.playlists.values():
                p.sort_songs()
            print("All playlists songs have been sorted by name ")


        # Option 9 shuffle songs in a  playlist 
        elif choice == "9":
            playlist_name = input_not_empty("playlist name to shuffle: ")
            p = svc.playlists.get(playlist_name)
            if not p: 
                print("Playlist not found")
                continue
            p.shuffle_song()
            print(f"Shuffled songs in playlist '{playlist_name}'")
        
        #option 10 export playlist to a text file
        elif choice == "10":
            out = input_not_empty("export file path (data/export_playlist.txt): ")
            svc.export_file(out)
            print(f"Export playlist to {out}")

        #Option 11 loading a playlist from a text file
        elif choice == "11":
            path = input_not_empty("Sample file path (e.g data/sample_playlist.txt): ")

            try:
                svc.add_playlist_from_file(path)
                print("loaded playlist from a file")
            except Exception as e:
                print(f"Failed to load: {e}")


        # option 12 display all playlist and their songs
        elif choice == "12":
            if not svc.playlists:
                print("no playlist available")
            else:
                for playlist_name, p in svc.playlists.items():
                    print(p.to_text_block())

                    print()


        else:
            print("invalid option. please try again")

if __name__ == "__main__":
    main()








