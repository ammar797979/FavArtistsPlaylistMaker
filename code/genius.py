import time
import lyricsgenius as lg
import spotify as sp

GENIUS_ACCESS_TOKEN = "GENIUS_ACCESS_TOKEN"

genius = lg.Genius(GENIUS_ACCESS_TOKEN, timeout=15, retries=3)

def find_artists_songs(artist_name):
    '''
    Find all songs associated with an artist on Genius and get their Spotify URIs

    :param artist_name: Name of the artist to search for
    :return: A list of tuples containing (song name, primary artist, Spotify URI) for found tracks
    '''
    artist_songs_on_genius = []
    song_artist_uri_tuple = []
    
    print(f"Finding ALL songs associated with {artist_name} on Genius...")

    print("\n\nIGNORE THE FOLLOWING LINES BETWEEN THE ASTERISKS")
    print("***********************************************************************")
    artist = None
    try:
        artist = genius.search_artist(artist_name, get_full_info=False, max_songs=0)
    except Exception as e:
        print(f"First attempt failed ({e}). Retrying in 2 seconds...")
        time.sleep(2)
        try:
            artist = genius.search_artist(artist_name, get_full_info=False, max_songs=0)
        except Exception as e2:
            print(f"Critical Error searching for artist {e2}.\n")
            return []
    print("***********************************************************************")
    print("IGNORE THE ABOVE LINES BETWEEN THE ASTERISKS\n\n")

    if artist is not None:
        print(f"Found artist: {artist.name} (ID: {artist._body['id']})")
        page = 1
        while page:
            print(f"  Fetching page {page} of songs from Genius...")
            res = genius.artist_songs(artist._body['id'], sort='popularity', per_page=50, page=page)
            if res and 'songs' in res:
                for song in res['songs']:
                    artist_songs_on_genius.append(song)
                    print(f"    Found song: {song['title']}")
            page = res.get('next_page')
        print(f"Found {len(artist_songs_on_genius)} songs for {artist_name} on Genius.\n")
        i = 0
        for song in artist_songs_on_genius:
            title = song['title']
            primary_artist = song['primary_artist']['name']
            search_query = f"{title} {primary_artist}"
            print(f"Searching Spotify for: {title} by {primary_artist}...")
            track = sp.find_song(search_query)
            if track is None:
                print(f"    No match found on Spotify for: {title} by {primary_artist}, skipping...")
            else:
                i += 1
                song_artist_uri_tuple.append(track)
                print(f"    Found Spotify track: {track[0]} by {track[1]} (URI: {track[2]})")
            print()
        print(f"Total Spotify tracks found for {artist_name}: {i}")
    else:
        print(f"No artist found for {artist_name} on Genius, continuing to next artist.")
    return song_artist_uri_tuple

        