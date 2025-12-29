import genius as gen
import spotify as sp
import gui
import logger

# Get inputs from GUI
playlist_name, artists_to_search, log_filename = gui.get_user_inputs()

# Setup logging
logger.setup_logging(log_filename)

unique_track_tuples = {}

# 1. Test connection
connected = sp.connect("start")
if connected is True:
    print("Successfully connected to Spotify!\n")
elif connected is None:
    print("Failed to connect to Spotify due to authorization error. Exiting program.")
    input("Press Enter to exit...")
else:
    print(f"Failed to connect to Spotify, HTTP Status Code: {connected}. Exiting program.")
    input("Press Enter to exit...")


# 2. Find songs for each artist and collect unique URIs
for artist in artists_to_search:
    artist_tracks = gen.find_artists_songs(artist)
    for track in artist_tracks:
        if track[2] in unique_track_tuples:
            print(f"Duplicate track found, dropping an entry of: {track[0]} by {track[1]} (URI: {track[2]})")
        else:
            unique_track_tuples[track[2]] = (track[0], track[1])
    print("\n****************************************************************\n")
print(f"Total unique tracks found: {len(unique_track_tuples)}\n")
# 3. Find (and re-create from scratch) or create playlist
playlist_id = sp.find_or_create_playlist(playlist_name)

# 4. Add tracks to playlist in batches of 100 (Spotify API limit)
if unique_track_tuples and playlist_id:
    unique_track_uris = list(unique_track_tuples.keys())
    sp.populate_playlist(playlist_id, unique_track_uris)

sp.print_added_tracks(unique_track_tuples)
input("Process complete! Press Enter to exit...")