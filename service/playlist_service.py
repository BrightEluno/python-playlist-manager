"""
This Service manage multiple playlist and Input/Output operations
"""

import os
from typing import Dict, List
from models.song import Song
from models.playlist import Playlist


class PlaylistService:
    """This class manage collection of the playlists"""

    def __init__(self):
        self.playlists: Dict[str, Playlist] = {}

    def create_playlist(self, name: str) -> Playlist:
        """ This function creates new playlist and store it in the playlist collection. This also Trims whitespace from the the playlist name, prevent duplicate playlist name,l and returns the new created Playlist object."""

        key = name.strip()

        # Checking if the playlist with the same name already exists
        if key in self.playlists:
            raise ValueError(f"Playlist '{name}' already exists")

        pl = Playlist(name=key)
        self.playlists[key] = pl

        return pl
    
    def delete_playlist(self, name: str) ->bool:
        """Deleting a playlist by name """
        key = name.strip()
        if key in self.playlists:
            del self.playlists[key]
            return True
        return False
    

    def rename_playlist(self, old_name: str, new_name: str) -> bool:
        """This function is for renaming existing playlist. this returns False if the old playlist dose not exist, raise valueError if the playlist with the new name already exist and returns True if renaming was suseccful """

        old_key = old_name.strip()
        new_key = new_name.strip()

        # Checking if the old playlist exists
        if old_key not in self.playlists:
            return False

        # Preventing duplicate names
        if new_key in self.playlists:
            raise ValueError(f"Playlist '{new_name}' already exists")

        # Rename and update the playlist in the collection
        pl = self.playlists.pop(old_key)
        pl.rename(new_key)
        self.playlists[new_key] = pl
        return True

    def add_song_to_playlist(self, playlist_name: str, song: Song) -> None:
        """ This function add song to a specified playlist and if the playlist does not exist it creates a new playlist"""

        key = playlist_name.strip()

        if key not in self.playlists:
            self.create_playlist(key)

        self.playlists[key].add_song(song)

    def remove_song_from_playlist(self, playlist_name: str, song_name: str, singer: str = None) -> bool:
        """ This function remove song from a specified playlist, returns False if the playlist does not exist, remove the song by name and optionally by singer name """

        key = playlist_name.strip()

        # Checking if the playlist exists
        if key not in self.playlists:
            return False

        # Remove the song from the playlist
        return self.playlists[key].remove_song(song_name, singer)

    def find_duplicates(self) -> List[str]:
        """This function return list of playlist name that contain duplicate songs across playlists """

        song_map = {}
        for playlist_name, p in self.playlists.items():
            for s in p.songs:
                k = s.key()
                song_map.setdefault(k, set()).add(playlist_name)
        
        duplicated_playlist = set()
        for k, playlist_name in song_map.items():
            if len(playlist_name) > 1:
                duplicated_playlist.update(playlist_name)
        return sorted(duplicated_playlist)
        
    def sort_by_name(self):
        """ This return a list of playlist sorted by name in ascending other"""
        return [self.playlists[k] for k in sorted(self.playlists.keys(), key=lambda x: x.strip().lower())]
    

    def export_file(self, file_path: str) -> None:
        """ This exports all the playlists and thir songs to a text file in a readable format."""

        dirpath = os.path.dirname(file_path)

        if dirpath : 
            os.makedirs(dirpath, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            for playlist_name in sorted(self.playlists.keys(), key=lambda x: x.strip().lower()):
                p =self.playlists[playlist_name]
                f.write(p.to_text_block())
                f.write("\n\n")

    def add_playlist_from_file(self, file_path: str) -> None:
        """This function loads playlist from a text file format.
        """

        #Checking if the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(file_path)
        
        #This read the entire file content
        with open(file_path, "r", encoding="utf-8") as f :
            content = f.read()
        
        #Splitting the file into sections separated by blank lines 
        sections = [s.strip() for s in content.split('\n\n') if s.strip()]

        for se in sections:
            #Split each section into non empty lines
            lines = [l.strip() for l in se.splitlines() if l.strip()]
            if not lines:
                continue
            
            #The playlist header should be the first in line
            header = lines[0]
            if not header.lower().startswith("playlist:"): continue

            #extracting playlist name and creating the playlist

            playlist_name = header.split(":", 1)[1].strip()

            if playlist_name in self.playlists:
                p = self.create_playlist(playlist_name)
            else:
                p= self.create_playlist(playlist_name)
            
            #Process each song entry in the playlist
            for line in lines[1:]:
                if line.startswith("-"):
                    parts = [part.strip() for part in line[1:].split("|")]

                    if len(parts) >= 3:
                        name, singer, genre = parts[0], parts[1],parts[2]
                    elif len(parts) == 2:
                        name, singer = parts[0], parts[1]
                        genre  = "Unknown"
                    else:
                        continue

                    #Add the song to the playlist
                    p.add_song(Song(name=name, singer=singer, genre=genre))        
