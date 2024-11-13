import os
import subprocess
import threading
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog
from pytubefix import YouTube
import re  # To clean up invalid characters from filenames
import shutil


# Browse function to select download directory
def browse():
    download_directory = filedialog.askdirectory(initialdir=os.path.expanduser("~"), title="Select Download Directory")
    download_path.set(download_directory)


def check_ffmpeg():
    if not shutil.which("ffmpeg"):
        messagebox.showerror("Error", "FFmpeg is required but not found. Please install it or include it in the same directory as this application.")
        return False
    return True


# Function to run the download in a separate thread
def start_download_thread():
    if not check_ffmpeg():  # Ensure ffmpeg is available
        return  # Exit if ffmpeg is missing
    # Disable the download button to prevent multiple clicks
    download_button.config(state=tk.DISABLED)
    # Start the download in a new thread
    threading.Thread(target=download).start()


# Function to clean up the filename by removing invalid characters
def clean_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename)


# Function to reset the UI after download
def reset_ui():
    # Clear the input fields
    video_link.set("")
    download_path.set("")
    filename.set("")
    # Reset the progress bar
    progress_bar["value"] = 0
    # Clear the status label
    status_label.config(text="")
    root.update_idletasks()  # Update the UI


# Download function (runs in a separate thread)
def download():
    url = video_link.get()
    folder = download_path.get()
    custom_name = clean_filename(filename.get())  # Clean up the filename

    if not url or not folder or not custom_name:
        messagebox.showerror("Error", "Please enter a valid YouTube URL, select a destination folder, and provide a filename.")
        download_button.config(state=tk.NORMAL)
        return

    try:
        yt = YouTube(url, on_progress_callback=on_progress_update)

        # Update status label
        status_label.config(text="Downloading video...")

        # Get highest resolution video (adaptive)
        video_stream = yt.streams.filter(adaptive=True, file_extension="mp4").order_by("resolution").desc().first()
        if not video_stream:
            raise Exception("No video stream found.")
        print(f"Downloading video in resolution: {video_stream.resolution}")
        video_path = video_stream.download(output_path=folder, filename=f"{custom_name}_video.mp4")

        # Update status label
        status_label.config(text="Downloading audio...")

        # Get highest quality audio
        audio_stream = yt.streams.filter(only_audio=True).first()
        if not audio_stream:
            raise Exception("No audio stream found.")
        print("Downloading audio...")
        audio_path = audio_stream.download(output_path=folder, filename=f"{custom_name}_audio.mp4")

        # Update status label
        status_label.config(text="Merging video and audio...")

        # Merge video and audio using ffmpeg
        output_path = os.path.join(folder, f"{custom_name}.mp4")
        # ffmpeg_cmd = f'ffmpeg -i "{video_path}" -i "{audio_path}" -c:v copy -c:a aac "{output_path}"'
        ffmpeg_cmd = f'./ffmpeg -i "{video_path}" -i "{audio_path}" -c:v copy -c:a aac "{output_path}"'

        subprocess.run(ffmpeg_cmd, shell=True)

        # Delete the intermediate video and audio files
        try:
            os.remove(video_path)
            os.remove(audio_path)
            print("Deleted intermediate video and audio files.")
        except Exception as e:
            print(f"Error deleting files: {e}")

        # Download captions if available
        try:
            caption = yt.captions.get('a.en')
            if caption:
                caption.save_captions(os.path.join(folder, f"{custom_name}_captions.txt"))
                print("Captions downloaded.")
            else:
                print("No captions available.")
        except Exception as e:
            print(f"Error downloading captions: {e}")

        # Update status label
        status_label.config(text="Download completed!")
        messagebox.showinfo("Success", f"Downloaded and saved in:\n{folder}")
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", f"Failed to download video. Error: {e}")
    finally:
        # Re-enable the download button after the download completes
        download_button.config(state=tk.NORMAL)
        reset_ui()  # Reset the UI for the next download


# Progress bar update function
def on_progress_update(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    progress_bar["value"] = percentage
    root.update_idletasks()  # Update the progress bar


# Function to create UI widgets
def create_widgets():
    # Configure grid layout to adjust column weights
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Define colors
    colour1 = "#020f12"
    colour2 = "#05d7ff"
    colour3 = "#65e7ff"
    colour4 = "BLACK"

    # Main frame for content with padding on all sides
    main_frame = tk.Frame(root, bg=colour1, padx=20, pady=20)
    main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    # Configure columns to ensure equal space distribution
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=2)
    main_frame.columnconfigure(2, weight=1)

    # Header Label
    header_label = tk.Label(main_frame, text="YouTube Video Downloader", font=("SegoeUI", 20, "bold"), bg="white", fg="black")
    header_label.grid(row=0, column=0, columnspan=3, pady=20, sticky="ew")

    # YouTube Link Label and Entry
    link_label = tk.Label(main_frame, text="YouTube URL:", font=("Segoe UI", 16, "bold"), bg="white", fg="black", anchor="w")
    link_label.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    root.link_text = tk.Entry(main_frame, width=40, textvariable=video_link, font=("Segoe UI", 16, "bold"), bd=1, relief=tk.FLAT, bg="white", fg="black")
    root.link_text.grid(row=1, column=1, padx=10, pady=10, columnspan=2, sticky="ew")

    # Filename Label and Entry
    filename_label = tk.Label(main_frame, text="Filename:", font=("Segoe UI", 16, "bold"), bg="white", fg="black", anchor="w")
    filename_label.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    root.filename_text = tk.Entry(main_frame, width=30, textvariable=filename, font=("Segoe UI", 16, "bold"), bd=1, relief=tk.FLAT, bg="white", fg="black")
    root.filename_text.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

    # Destination Label, Entry, and Browse Button
    destination_label = tk.Label(main_frame, text="Destination:", font=("Segoe UI", 16, "bold"), bg="white", fg="black", anchor="w")
    destination_label.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    root.destination_text = tk.Entry(main_frame, width=30, textvariable=download_path, font=("Segoe UI", 16, "bold"), bd=1, relief=tk.FLAT, bg="white", fg="black")
    root.destination_text.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

    browse_button = tk.Button(main_frame, text="Browse", command=browse, bg=colour2, fg="black", font=("Segoe UI", 16, "bold"), width=10)
    browse_button.grid(row=3, column=2, padx=10, pady=10, sticky="ew")

    # Download Button
    global download_button
    download_button = tk.Button(main_frame, text="Download Video", command=start_download_thread, bg=colour2, fg="black", font=("Segoe UI", 16, "bold"), width=20)
    download_button.grid(row=4, column=0, columnspan=3, pady=20, sticky="ew")

    # Progress Bar
    global progress_bar
    progress_bar = tk.ttk.Progressbar(main_frame, orient="horizontal", length=400, mode="determinate")
    progress_bar.grid(row=5, column=0, columnspan=3, pady=10, padx=20, sticky="ew")

    # Status Label (to display messages during download)
    global status_label
    status_label = tk.Label(main_frame, text="", font=("Segoe UI", 14), bg=colour1, fg="white")
    status_label.grid(row=6, column=0, columnspan=3, pady=10, sticky="ew")


# Main GUI setup
root = tk.Tk()
root.geometry("800x500")
root.resizable(False, False)
root.title("YouTube Video Downloader")
root.config(bg="white")

# Variables
video_link = tk.StringVar()
download_path = tk.StringVar()
filename = tk.StringVar()  # New variable for filename

# Create UI widgets
create_widgets()

# Run the main loop
root.mainloop()
