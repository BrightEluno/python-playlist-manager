from models.user import User
from models.song import Song
import os
from service.playlist_service import PlaylistService
import os
from service.authentication_service import AuthenticationService


# Authentication Testing


def test_login_success():
    #Test that login succeeds when correct username and password is provided
    auth = AuthenticationService(User("user123", "Givemetheykey123"))
    assert auth.login_attempt("user123", "Givemetheykey123") is True

def test_login_failure():
    # Testing that the login fails when incorrect credentials are provided
    auth = AuthenticationService(User("user123", "Givemetheykey123"))
    assert auth.login_attempt("wrongUser", "wrongPassword") is False

def test_login_lock():
    #Testing that the account is locked after three failed login attempts

    auth = AuthenticationService(User("user123", "Givemetheykey123"))

    #Performing three failed login attempts
    auth.login_attempt("wrong1", "wrong1")
    auth.login_attempt("wrong2", "wrong2")
    auth.login_attempt("wrong3", "wrong3")

    assert auth.locked() is True


# Test for playlist Creation and Deleting

def test_create_playlist():
    # Test that the playlist is successfully created and stored

    svc = PlaylistService()
    svc.create_playlist("Playlist")

    assert "Playlist" in svc.playlists


def test_delete_playlist():
    # Testing if an existing playlist can be deleted
    svc =PlaylistService()
    svc.create_playlist("DeletePlaylist")

    result = svc.delete_playlist("DeletePlaylist")
    assert result is True
    assert "DeletePlaylist"  not in svc.playlists

# Test for removing adding and songs on playlist


def test_add_song_to_playlist():
    # Test that a song can be added to a playlist

    svc = PlaylistService()
    svc.add_song_to_playlist("Afro", Song("Love", "Burna boy", "Afro"))

    assert len(svc.playlists["Afro"].songs) ==1

def test_remove_song_from_playlist():
    # Testing that a song can be removed from a playlist

    svc = PlaylistService()
    svc.add_song_to_playlist("Afro", Song("Love", "Burna boy", "Afro"))

    removed = svc.remove_song_from_playlist("Afro", "Love")
    assert removed is True
    assert len(svc.playlists["Afro"].songs) == 0


# Test for changing song details

def test_change_song_details():
    # This tests if a song details can be updated
    svc = PlaylistService()
    svc.add_song_to_playlist("Rap", Song("History", "Dave", "Rap"))
    
    #find the song and update its detail
    song = svc.playlists["Rap"].find_song("History")
    song.update(name="123 Months", genre="Hip-hop")

    # Verify the changes
    assert song.name == "123 Months"
    assert song.genre == "Hip-hop"


# Test for Renaming playlist

def test_rename_playlist():
    # test that an existing playlist can be renamed 

    svc = PlaylistService()
    svc.create_playlist("OldName")

    renamed = svc.rename_playlist("OldName", "NewName")

    assert renamed is True
    assert "NewName" in svc.playlists
    assert "OldName" not in svc.playlists


# Test for sorting

def test_sort_song_in_playlist():
    # Test that songs within a playlist can be sorted alphabetically by song name 
    svc = PlaylistService()
    svc.add_song_to_playlist("Love Songs", Song("Love", "Burna boy", "Afro"))
    svc.add_song_to_playlist("Love Songs", Song("All The Love", "Ayra Starr", "Afro"))

    playlist = svc.playlists["Love Songs"]
    playlist.sort_songs()

    assert playlist.songs[1].name == "Love"

def test_sort_playlists():
    # Test that the playlist can be sorted alphabetically by name
    svc = PlaylistService()
    svc.create_playlist("Afro")
    svc.create_playlist("Love Song")

    sorted_playlist = svc.sort_by_name()
    name = [p.name for p in sorted_playlist]
    assert name == ["Afro", "Love Song"]


# Test for duplicate song detection

def test_find_duplicate_song_across_playlist():
    # Testing for detection of duplicate songs across multiple playlist

    svc = PlaylistService()
    

    #Adding two song with the same name to a playlist
    svc.add_song_to_playlist("Love Songs", Song("Love", "Burna boy", "Afro"))
    svc.add_song_to_playlist("Afro", Song("Love", "Burna boy", "Afro"))

    duplicates = svc.find_duplicates()
    assert "Love Songs" in duplicates
    assert "Afro" in duplicates
    

# Test shuffle songs 

def test_shuffle_songs():
    # Test that shuffling a playlist changes the order without losing or duplicating any song

    svc = PlaylistService()
    svc.add_song_to_playlist("Love Songs", Song("Love", "Burna boy", "Afro"))
    svc.add_song_to_playlist("Love Songs", Song("Love nwantiti", "CKay", "Afro"))
    svc.add_song_to_playlist("Love Songs", Song("All The Love", "Ayra Starr", "Afro"))

    playlist = svc.playlists["Love Songs"]

    #This captures the original order of songs
    original_order = [s.name for s in playlist.songs]

    #Shuffle the songs
    playlist.shuffle_song()
    shuffled_order =[s.name for s in playlist.songs]

    # verify that all song are still present after shuffling
    assert set(original_order) == set(shuffled_order)

# Test for exporting file

def test_export_playlist_to_file(tmp_path):
    # Test that playlist is exported correctly to s text file
    svc = PlaylistService()
    svc.add_song_to_playlist("Love Songs", Song("All The Love", "Ayra Starr", "Afro"))
    
    # Defining the export file path using pytest temporary directory

    file_path = tmp_path / "Songs.txt"

    #Export playlist to file 
    svc.export_file(str(file_path))

    #Verify that the file was created
    assert os.path.exists(file_path)

    #Reading and validating the  file contents

    content = file_path.read_text()
    assert "Playlist: Love Songs" in content
    assert "All The Love" in content




