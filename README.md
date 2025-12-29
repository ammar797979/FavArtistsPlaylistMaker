
# Fav Artists’ Playlist Maker
Make a Spotify playlist with **all** the songs tied to your favorite artists (even the ones they only wrote/produced or were uncredited on) using Genius for discovery and Spotify for playback. One-click GUI, packaged as a standalone `.exe`.


## Contents
-  [What The App Does](#what-the-app-does)
- [Authorization (Important)](#authorization)
-  [Quickstart (Windows Users)](#quickstart-windows-users)
- [Quickstart (Mac / Linux Users)](#quickstart-mac--linux-users)
-  [For Developers](#for-developers)
-  [Additional Note (If Not Approved)](#additional-note-if-not-approved)
-  [Notes On Accuracy (API Quirks)](#notes-on-accuracy-api-quirks)
-  [Playlist & Files Created](#playlist--files-created)
-  [Tech Stack](#tech-stack)
-  [Project Structure (Key Files)](#project-structure-key-files)
-  [License](#license)


You want a playlist with **everything** from an artist: songs they sang, wrote, produced, featured on, where the artist is a background artist hiding in the credits, or is uncredited totally. Doing that by hand is painful (duplicates, hidden tracks, similar names). This tool automates it.
(Note: I am currently working on a tool that makes a similar playlist with only the songs where the specified artist is one of the main artists)


## What The App Does
Launch the app, fill in the GUI, and a few seconds/minutes later (depends on artists/song count) you get a Spotify playlist with all the tracks Genius can find for those artists. Duplicates are skipped by URI; non-primary/“background” credits are included.
The duplicate removal logic helps if multiple artists are requested and they worked on the same songs.


## Authorization
Due to requirements from Spotify API, users need to be added to a client whitelist by the developer to be able to use the app. To do so, please reach out at: ammarsohail79@gmail.com

**Important**: You can email me from whatever email you like, but please mention the email linked to your Spotify account, I cannot whitelist your account without knowing that email.

*Alternatively,* you could simply follow the steps [here](#additional-note-if-not-approved), but for that you will need to also do the setup [for developers](#for-developers).

## Quickstart (Windows Users)
1) Download the latest `.exe` from [Releases](https://github.com/ammar797979/FavArtistsPlaylistMaker/releases/tag/v1.0).
2) The following steps assume you have read [Authorization](#authorization).
3) Run it; a browser opens for Spotify login/consent on first run (a `.cache` file appears beside the exe to skip future logins).
4) In the GUI, enter:
	- Playlist name (warning: an existing playlist with that name will be overwritten).
	- Artists (comma-separated), capitalization should not matter (ideally).
	- Log filename (a `.txt` is created next to the exe; the real-time console logs will be stored in the file as well).
5) Click **Create Playlist** and watch the logs. Tip: turn on shuffle when listening to the playlist in Spotify if you don’t want artist-by-artist order.


## Quickstart (Mac / Linux Users)
Since the standalone executable is Windows-only, please run from source:
1) Install [Python 3](https://www.python.org/downloads/).
2) Download this repository (Code -> Download ZIP) and unzip it.
3) Open a terminal in that folder.
4) Install dependencies: `pip install -r requirements.txt`
2) The following step assumes you have read [Authorization](#authorization).
5) Run the app: `python main.py`, the rest of the steps can be followed from step 3 in [Quickstart (Windows Users)](#quickstart-windows-users)


## For Developers
1) Clone the repo.
2) Install deps: `pip install -r requirements.txt`.
3) Get a Genius API token: https://genius.com/api-clients.
4) Put the token in `genius.py` in place of `GENIUS_ACCESS_TOKEN`.
5) Run: `python main.py`.
6) Optional build: `python -m PyInstaller --onefile --name "FavArtists_Playlist_Maker" main.py`.


## Additional Note (If Not Approved)
If I can’t add you to my Spotify client whitelist, or am unresponsive, you can create your own client at https://developer.spotify.com/ and drop your `CLIENT_ID` into `spotify.py`.


## Notes On Accuracy (API Quirks)
- Expect ~5–15% mismatches on catalogs: unreleased/planned tracks are sometimes on Genius, while Spotify search grabs a similar named song/artist sometimes, and even mixes up the song name with the artist's name. Discrepancies also show up in scenarios where a song has the same name as its album.
- If a random track shows up, it might be from your preferred artist, but the artist was not a main artist for that song. You can confirm by clicking the `...(three dots)->View Credits` next to that song on Spotify or check your artists discography on Genius. Otherwise, it’s likely an API search mismatch; just remove it manually.


## Playlist & Files Created
-  **Cache**: `.cache*` beside the exe to reuse Spotify auth; delete to force re-login.
-  **Log file**: Named in the GUI; created where the exe lives; mirrors console output.
-  **Playlist overwrite**: Same-name playlist is cleared and repopulated, or a new one is created if same-name playlist non-existent.


## Tech Stack
- Python 3
- Spotipy (Spotify API, PKCE auth)
- LyricsGenius (Genius API)
- Tkinter (GUI)
- PyInstaller (packaging)


## Project Structure (Key Files)
-  `main.py` — Orchestrates flow; kept minimal and clean.
-  `gui.py` — Tkinter UI for inputs.
-  `logger.py` — Dual writer to console + log file.
-  `spotify.py` — PKCE auth, search song, playlist create/replace, populate playlist, log final songs added to playlist.
-  `genius.py` — Genius artist search, song harvesting, Spotify matching.
-  `.gitignore` — Excludes venv, build/dist, caches, logs; allows `requirements.txt`.


## License
MIT License. See `LICENSE` for details.
