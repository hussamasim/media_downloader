import re
import tkinter as tk
from tkinter import ttk, filedialog
import yt_dlp

def get_input():
    url = urlTextBox.get()
    if formatVar.get() == 1:
        download_mp3(url)
    elif formatVar.get() == 0:
        download_mp4(url)

def download_mp3(url):
    # Get the selected folder path from the destination_var
    destination_folder = destination_var.get()

    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}],
        "outtmpl": f"{destination_folder}/%(title)s.%(ext)s",  # Set the output template
        "progress_hooks": [progress_hook],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydlp:
        ydlp.download([url])


def download_mp4(url):
    # Get the selected folder path from the destination_var
    destination_folder = destination_var.get()

    ydl_opts = {
        "format": "best",
        "outtmpl": f"{destination_folder}/%(title)s.%(ext)s",  # Set the output template
        "progress_hooks": [progress_hook],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydlp:
        ydlp.download([url])

def remove_escape_sequences(text):
    # Use regex to remove escape sequences (color codes) from the text
    return re.sub(r'\x1b\[[0-9;]*m', '', text)

def progress_hook(d):
    if d['status'] == 'downloading':
        progress_str = remove_escape_sequences(d['_percent_str'])
        progress = re.search(r'\b\d+(\.\d+)?\b', progress_str)
        if progress:
            percent = float(progress.group())
            progress_var.set(percent)

def browse_destination():
    folder_path = filedialog.askdirectory()
    if folder_path:
        destination_var.set(folder_path)

# GUI Elements:
root = tk.Tk()
root.title("Media Downloader")
urlLabel = tk.Label(root, text="YouTube URL:")
urlTextBox = tk.Entry(root, width=100)

formatVar = tk.IntVar()

mp3Check = tk.Radiobutton(root, text="MP3", variable=formatVar, value=1)
mp4Check = tk.Radiobutton(root, text="MP4", variable=formatVar, value=0)

downloadButton = tk.Button(root, text="Download", width=10, command=get_input)

# Progress Bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, length=200)

# Button to open folder location browse
browseButton = tk.Button(root, text="Browse", width=10, command=browse_destination)
browseButton.grid(row=2, column=3)

destination_var = tk.StringVar()
destination_entry = tk.Entry(root, width=100, textvariable=destination_var, state="readonly")
destination_entry.grid(row=2, column=1, columnspan=2)

# GUI Formatting:
root.geometry("800x480+400+240")
urlLabel.grid(row=0, column=0)
urlTextBox.grid(row=0, column=1)
mp3Check.grid(row=1, column=0)
mp4Check.grid(row=1, column=1)
downloadButton.grid(row=0, column=2)
progress_bar.grid(row=2, columnspan=3, pady=10)

root.mainloop()

# update UI
# file location save as
# error handling
# dynamic progress bar
# embed metadata option