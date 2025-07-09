import os
import tkinter as tk
from tkinter import messagebox, ttk
import yt_dlp
import threading

class YouTubeDownloader:
    def __init__(self, master):
        self.master = master
        self.master.title("YouTube Video Downloader")
        self.master.geometry("800x600")
        self.master.configure(bg='lightblue')

        self.url_label = tk.Label(master, text="Enter YouTube Video URL:", bg='lightblue')
        self.url_label.pack(pady=10)

        self.url_entry = tk.Entry(master, width=70)
        self.url_entry.pack(pady=5)

        self.quality_label = tk.Label(master, text="Select Video Quality:", bg='lightblue')
        self.quality_label.pack(pady=10)

        self.quality_var = tk.StringVar(value='best')
        self.quality_options = ['360p', '480p', '720p', '1080p', '2160p', 'best']
        self.quality_menu = ttk.Combobox(master, textvariable=self.quality_var, values=self.quality_options)
        self.quality_menu.pack(pady=5)

        self.download_button = tk.Button(master, text="Download Video", command=self.download_video)
        self.download_button.pack(pady=20)

        self.status_label = tk.Label(master, text="", bg='lightblue')
        self.status_label.pack(pady=5)

    def download_video(self):
        video_url = self.url_entry.get()
        
        if not video_url:
            messagebox.showerror("Error", "Please enter a valid URL.")
            return
        
        threading.Thread(target=self._download_video_thread, args=(video_url,)).start()

    def _download_video_thread(self, video_url):
        download_dir = 'C:/Users/balak/Downloads/ytube/Downloads'
        os.makedirs(download_dir, exist_ok=True)

        selected_quality = self.quality_var.get()
        
        ydl_opts = {
            'format': f'bestvideo[height<={selected_quality[:-1]}]+bestaudio/best' if selected_quality != 'best' else 'best',
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
