import os
import shutil
import tkinter as tk
from tkinter import messagebox
import yt_dlp

# Function to download videos
def download_videos():
    playlist_url = url_entry.get()
    download_dir = 'C:/Users/balak/Downloads/ytube/Downloads'
    
    os.makedirs(download_dir, exist_ok=True)

    ydl_opts = {
        'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])
        
        # Create a zip archive of the downloaded files
        shutil.make_archive(download_dir, 'zip', download_dir)
        messagebox.showinfo("Success", f'Playlist downloaded and zipped successfully.\nFind the zip file: {download_dir}.zip')
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Setting up the GUI window
root = tk.Tk()
root.title("YouTube Playlist Downloader")

# URL input label and entry
url_label = tk.Label(root, text="Enter YouTube Playlist URL:")
url_label.pack(pady=10)

url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Download button
download_button = tk.Button(root, text="Download", command=download_videos)
download_button.pack(pady=20)

# Run the application
root.mainloop()
