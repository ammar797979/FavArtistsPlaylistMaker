import tkinter as tk
from tkinter import messagebox
import sys

def get_user_inputs():
    """
    Opens a GUI window to get user configuration.
    :return: A tuple: (playlist_name, [artist_list], log_filename)
    """
    result = {"playlist": None, "artists": None, "log": None}
    
    def on_start():
        # 1. Get Playlist
        playlist_name = entry_playlist.get().strip()
        if not playlist_name:
            playlist_name = "Fav Artists"
            
        # 2. Get Artists
        artists_raw = entry_artists.get().strip()
        if not artists_raw:
            messagebox.showerror("Error", "Please enter at least one artist.")
            return
        artists = [x.strip() for x in artists_raw.split(',') if x.strip()]
        
        # 3. Get Log File
        logfile_name = entry_log.get().strip()
        if not logfile_name:
            logfile_name = "spotify_log.txt"
        if not logfile_name.endswith(".txt"):
            logfile_name += ".txt"
            
        # Save to result and close
        result["playlist"] = playlist_name
        result["artists"] = artists
        result["log"] = logfile_name
        root.destroy()

    # --- GUI SETUP ---
    root = tk.Tk()
    root.title("Fav Artists' Playlist Maker")
    root.geometry("450x400")
    
    # Playlist Label & Entry
    tk.Label(root, text="Playlist Name:", font=("Arial", 10, "bold")).pack(pady=(20, 5))
    tk.Label(root, text="Note: If a playlist with the same name exists, it will be overwritten.", font=("Arial", 8, "italic")).pack()
    entry_playlist = tk.Entry(root, width=40)
    entry_playlist.insert(0, "Fav Artists")
    entry_playlist.pack()
    
    # Artists Label & Entry
    tk.Label(root, text="Artists (comma separated):", font=("Arial", 10, "bold")).pack(pady=(20, 5))
    tk.Label(root, text="e.g. GOAT Verse, Mosquito Melodies, e.t.c", font=("Arial", 8, "italic")).pack()
    entry_artists = tk.Entry(root, width=40)
    entry_artists.pack()
    
    # Log File Label & Entry
    tk.Label(root, text="Log Filename:", font=("Arial", 10, "bold")).pack(pady=(20, 5))
    tk.Label(root, text="This file will be created in the folder where you ran the program.", font=("Arial", 8, "italic")).pack()
    entry_log = tk.Entry(root, width=40)
    entry_log.insert(0, "spotify_log.txt")
    entry_log.pack()
    
    # Start Button
    btn_start = tk.Button(root, text="Create Playlist", command=on_start, bg="#1DB954", fg="white", font=("Arial", 12, "bold"), height=2, width=20)
    btn_start.pack(pady=30)
    
    root.mainloop()
    
    # Return values (or exit if window was closed without clicking Start)
    if result["artists"] is None:
        sys.exit()
        
    return result["playlist"], result["artists"], result["log"]