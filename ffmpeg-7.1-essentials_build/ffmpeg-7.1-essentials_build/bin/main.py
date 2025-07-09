import os
import shutil
import tkinter as tk
from tkinter import messagebox, ttk
import yt_dlp
import threading

class YouTubeDownloader:
    def __init__(self, master):
        self.master = master
        self.master.title("YouTube Playlist Downloader")
        self.master.geometry("800x600")  # Increase window size
        self.master.configure(bg='lightblue')  # Change background color

        # URL input label and entry
        self.url_label = tk.Label(master, text="Enter YouTube Playlist URL:", bg='lightblue')
        self.url_label.pack(pady=10)

        self.url_entry = tk.Entry(master, width=70)
        self.url_entry.pack(pady=5)

        # Get video list button
        self.get_videos_button = tk.Button(master, text="Get Video List", command=self.get_video_list)
        self.get_videos_button.pack(pady=10)

        # Create a scrollable frame for video list
        self.create_scrollable_frame()

        # Download all button
        self.download_all_button = tk.Button(master, text="Download All", command=self.download_all_videos)
        self.download_all_button.pack(pady=20)

        # Download status label
        self.status_label = tk.Label(master, text="", bg='lightblue')
        self.status_label.pack(pady=5)

    def create_scrollable_frame(self):
        self.container = ttk.Frame(self.master)
        self.container.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.container)
        self.scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def get_video_list(self):
        playlist_url = self.url_entry.get()
        
        if not playlist_url:
            messagebox.showerror("Error", "Please enter a valid URL.")
            return
        
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'extract_flat': True,
            'quiet': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                playlist_info = ydl.extract_info(playlist_url, download=False)
                videos = playlist_info['entries']
                
                for widget in self.scrollable_frame.winfo_children():
                    widget.destroy()

                for video in videos:
                    title = video['title']
                    button = tk.Button(self.scrollable_frame, text=f"Download '{title}'", command=lambda url=video['url']: self.download_video(url))
                    button.pack(anchor='w', padx=10, pady=5)

                messagebox.showinfo("Success", f'Found {len(videos)} videos in the playlist.')
        
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def download_video(self, video_url):
        threading.Thread(target=self._download_video_thread, args=(video_url,)).start()

    def _download_video_thread(self, video_url):
        download_dir = 'C:/Users/balak/Downloads/ytube/Downloads'
        os.makedirs(download_dir, exist_ok=True)

        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
            'progress_hooks': [self.progress_hook],
            'quiet': True,
            'noprogress': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])

            self.update_status_message(f"Video downloaded successfully: {video_url}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def download_all_videos(self):
        playlist_url = self.url_entry.get()
        
        if not playlist_url:
            messagebox.showerror("Error", "Please enter a valid URL.")
            return
        
        threading.Thread(target=self._download_all_videos_thread, args=(playlist_url,)).start()

    def _download_all_videos_thread(self, playlist_url):
        download_dir = 'C:/Users/balak/Downloads/ytube/Downloads'
        os.makedirs(download_dir, exist_ok=True)

        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
            'progress_hooks': [self.progress_hook],
            'quiet': True,
            'noprogress': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([playlist_url])

            self.update_status_message(f'All videos downloaded successfully.')

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def progress_hook(self, d):
       if d['status'] == 'downloading':
           percent_str = d['_percent_str']
           speed_str = d['_speed_str']
           filename = d['filename']
           status_message = f"Downloading: {filename} - {percent_str} at {speed_str}"
           self.update_status_message(status_message)

    def update_status_message(self, message):
       self.status_label.config(text=message)
       self.master.after(2000, lambda: self.status_label.config(text=""))

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()
