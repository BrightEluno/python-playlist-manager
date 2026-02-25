
import random
from typing import List
from models.song import Song



class Playlist: 
    "" "Represents a playlist containing songs. """

    def __init__ (self, name: str):
        self.name = name
        self.songs: List [Song] = []
    
    def add_song(self, song: Song):
        """Add Song object to the playlist. """
        self.songs.append(song)

    def remove_song(self, song_name: str, singer: str = None) -> bool:
        """This function remove a song by name and optionally singer.
        It returns True if removed"""

        target = song_name.strip().lower()
        for i, s in enumerate (self.songs):
            if s.name.strip().lower() == target and (singer is None or s.singer.strip().lower() == singer.strip().lower()):
                del self.songs[i]
                return True
            
        return False
    

    def find_song(self, song_name: str, singer: str = None):
        """This function return the Song object if found, else it returns None."""

        target = song_name.strip().lower()   
        for s in self.songs:
            if s.name.strip().lower() == target and (singer is None or s.singer.strip().lower() == singer.strip().lower()):
                return s
        return None
    
    def rename(self, new_name: str) :
        """ This function rename playlist"""
        self.name = new_name

    def sort_songs(self):
        """this sort songs in playlist by name in ascending other"""
        self.songs.sort(key=lambda s: s.name.strip().lower())

    def shuffle_song(self):
        """ This shuffle the songs in the playlist randomly"""
        random.shuffle(self.songs)

    def to_text_block(self) -> str:
        """
        This convert the play list to a formatted multi-line text block.
        The output includes the name of the playlist in the first line, a numbered list of songs in the playlist, singer and genre.

        """
         

        #add each song to a numbered entry
        lines =[f"Playlist: {self.name}"]
        for i, s in enumerate(self.songs, start=1):
            lines.append(f"{i}. {s.name} | {s.singer} | {s.genre}")
        return "\n".join(lines)
    
    def __str__(self) -> str:
        # this displays the playlist name and the total number of songs in the playlist
        return f"{self.name} ({len(self.songs)}songs)"
