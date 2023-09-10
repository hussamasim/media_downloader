import re
import customtkinter as ctk
from tkinter import ttk, filedialog
import yt_dlp


# Taking input, downloading by type, progress bar
def get_input():
    url = url_input.get()
    if format_var.get() == 1:
        download_mp3(url)
    elif format_var.get() == 0:
        download_mp4(url)


def browse_destination():
    folder_path = filedialog.askdirectory()
    if folder_path:
        destination_var.set(folder_path)


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
            progress_bar.set(percent)


# making root and child widgets
root = ctk.CTk()
root.title("Media Downloader")
root.geometry("1280x720+400+240")

# making frames
heading1 = ctk.CTkFrame(root)
heading1.pack(fill=ctk.BOTH, expand="true")

heading2 = ctk.CTkFrame(root, fg_color="transparent")
heading2.pack(fill=ctk.BOTH, expand="true", padx=55)

heading3 = ctk.CTkFrame(root, fg_color="transparent")
heading3.pack(fill=ctk.BOTH, expand="true", padx=55)

heading4 = ctk.CTkFrame(root, fg_color="transparent")
heading4.pack(fill=ctk.BOTH, expand="true", padx=55)

# making fonts
heading_font = ctk.CTkFont(size=36, weight="bold")
subheading_font = ctk.CTkFont(size=28, weight="bold")
button_font = ctk.CTkFont(size=18, weight="bold")
body_font = ctk.CTkFont(size=12, weight="bold")

# making styles
button_style = ttk.Style()
button_style.configure("GreenButton",
                       font=ctk.CTkFont(size=18, weight="bold"),
                       fg_color="#1DB954",
                       bg_color="transparent",
                       hover_color="#10c650",
                       corner_radius=25,
                       border_width=0)

app_title = ctk.CTkLabel(heading1, font=heading_font, text="Media Downloader")

# choose URL elements
url_prompt = ctk.CTkLabel(heading2, font=subheading_font, text="Enter URL")
url_input = ctk.CTkEntry(heading2, width=1000, height=50, font=body_font,
                         placeholder_text="Ex. (https://www.youtube.com/...)", corner_radius=25, border_width=0)

download_media_button = ctk.CTkButton(heading2, width=10, height=50, font=button_font,
                                      text="Download", fg_color="#1DB954", hover_color="#10c650", corner_radius=25,
                                      border_width=0, command=get_input)

# file path elements
file_path_prompt = ctk.CTkLabel(heading3, text="Choose Destination", font=subheading_font)
destination_var = ctk.StringVar()
file_path = ctk.CTkEntry(heading3, width=1000, height=50, font=body_font, corner_radius=25, border_width=0,
                         textvariable=destination_var, state="readonly")

choose_file_button = ctk.CTkButton(heading3, width=10, height=50, font=button_font, text="Choose File",
                                   fg_color="#1DB954", hover_color="#10c650", corner_radius=25, border_width=0,
                                   command=browse_destination)

# file type elements
format_var = ctk.IntVar()
choose_type_font = ctk.CTkLabel(heading4, font=subheading_font, text="Choose File Type",)
mp3_radio_button = ctk.CTkRadioButton(heading4, text="MP3", fg_color="#1DB954", border_color="#1DB954",
                                      hover_color="#10c650", variable=format_var, value=1)
mp4_radio_button = ctk.CTkRadioButton(heading4, text="MP4", fg_color="#1DB954", border_color="#1DB954",
                                      hover_color="#10c650", variable=format_var, value=0)

# progress bar
progress_bar = ctk.CTkProgressBar(heading1, width=1280, height=25, fg_color="#2B2B2B", progress_color="#1DB954",
                                  corner_radius=0, variable=ctk.DoubleVar())

# formatting root and child widgets
app_title.pack(pady=100)

url_prompt.pack(pady=25)
url_input.pack(side="left")
download_media_button.pack(side="right", ipadx=15)

file_path_prompt.pack(pady=25)
file_path.pack(side="left")
choose_file_button.pack(side="right", ipadx=10)

choose_type_font.pack(pady=25)
mp3_radio_button.pack(pady=10)
mp4_radio_button.pack(pady=10)

progress_bar.pack(side=ctk.BOTTOM)

root.mainloop()
