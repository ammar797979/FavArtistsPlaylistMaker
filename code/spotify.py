import spotipy
from spotipy.oauth2 import SpotifyPKCE

# 1. SETUP
CLIENT_ID = "bf6ab79fc59144e39a75bb555f5da946"
REDIRECT_URI = "http://127.0.0.1:8888/callback"


sp_Client = spotipy.Spotify(auth_manager=SpotifyPKCE(
    client_id=CLIENT_ID,
    redirect_uri=REDIRECT_URI,
    scope="playlist-modify-public playlist-modify-private playlist-read-private user-library-read"
))

def connect(anystring):
    '''
    A dummy function to start Spotify connection

    :param anystring: literally anything, don't leave blank
    :return: None
    '''
    try:
        sp_Client.search(q=anystring, limit=1, type='track')
        return True
    # if 403, chances are, the user is not authorized by the developer
    except spotipy.exceptions.SpotifyException as e:
        if e.http_status == 403:
            print("ERROR: Spotify access forbidden. Make sure your Spotify account is authorized for this code by the developer.")
            return None
        else:
            return e.http_status

def find_song(query):
    '''
    Search for a song on Spotify and return its URI
    
    :param query: The search query string, ideally song title and artist
    :return: A tuple with the name, primary artist and Spotify URI of the found track, or None if not found
    '''
    res = sp_Client.search(q=query, limit=1, type='track')
    track = res['tracks']['items']

    if track:
        return (track[0]['name'], track[0]['artists'][0]['name'], track[0]['uri'])
    else:
        return None

def find_or_create_playlist(playlist_name):
    '''
    Find an existing playlist by name and empty it, or create a new one, then add tracks to it
    
    :param playlist_name: Name of the playlist to find or create
    :return: The Spotify ID of the found or created playlist
    '''
    current_user_playlists = sp_Client.current_user_playlists()
    existing_playlists = current_user_playlists['items']
    # Pagination for finding playlist, just ensures ALL playlists are covered
    while current_user_playlists['next']:
        current_user_playlists = sp_Client.next(current_user_playlists)
        existing_playlists.extend(current_user_playlists['items'])
    # Find the playlist by name, store its ID for altering playlist, then clear it if found
    playlist_id = None
    for playlist in existing_playlists:
        if playlist['name'] == playlist_name:
            playlist_id = playlist['id']
            print(f"Found existing playlist '{playlist_name}'. Clearing it...")
            sp_Client.playlist_replace_items(playlist_id, [])
            break
    # If not found, get user ID needed for playlist creation, then create new playlist
    if not playlist_id:
        print(f"Playlist with name '{playlist_name}' not found, creating new playlist: {playlist_name}")
        user_id = sp_Client.me()['id']
        new_playlist = sp_Client.user_playlist_create(user_id, playlist_name)
        # Store playlist ID for adding tracks
        playlist_id = new_playlist['id']
    return playlist_id

def populate_playlist(playlist_id, track_uris):
    '''
    Add tracks to a Spotify playlist in batches of 100

    :param playlist_id: The Spotify ID of the playlist to populate
    :param track_uris: List of Spotify track URIs to add to the playlist
    '''
    if track_uris:
        for i in range(0, len(track_uris), 100):
            sp_Client.playlist_add_items(playlist_id, track_uris[i:i+100])
        print(f"Updated playlist with {len(track_uris)} tracks.")
    else:
        print("No tracks to add to the playlist.")

def print_added_tracks(track_tuples):
    '''
    Print the list of added track names, artists and URIs

    :param track_tuples: Dict of Spotify track tuples that were added
    '''
    print("\nTracks added to playlist:")
    for track in track_tuples.keys():
        print(f" - {track_tuples[track][0]} by {track_tuples[track][1]} (URI: {track})")
    return None