# YouTube Video Downloader

A simple cross-platform YouTube video downloader with a graphical user interface (GUI) built using Python and `tkinter`. This application allows you to download videos and audio from YouTube, merge them, and save them locally on your computer.

## Features

- Download YouTube videos in the highest available resolution.
- Download and merge audio with video using `ffmpeg`.
- Custom filenames for downloaded videos.
- Download subtitles if available.
- Simple and intuitive GUI built with `tkinter`.
- Progress bar to show download progress.
- Supports Windows, macOS, and Linux.

## Requirements

- Python 3.7+
- [FFmpeg](https://ffmpeg.org/) installed or included in the app directory.
- Dependencies:
  - `pytube` (or `pytubefix` if using a modified version)
  - `tkinter` (included with standard Python installations)
  - `subprocess`, `threading`, `re` (standard libraries)

## Installation

### Step 1: Install Python

Make sure you have Python 3.7 or newer installed. You can download it from the [official website](https://www.python.org/downloads/).

### Step 2: Install Required Python Packages

Open a terminal/command prompt and install the required packages:

```bash
pip install pytube
pip install pyinstaller
```
### Step 3: Install FFmpeg

- Windows

- Download the FFmpeg static build from ffmpeg.org.
- Extract the downloaded zip file.
- Copy ffmpeg.exe from the bin folder into the same directory as the executable (yt_d2.exe).

- macOS

Install FFmpeg using Homebrew:
```bash
brew install ffmpeg
```
- Linux

Install FFmpeg using the package manager:
```bash
sudo apt install ffmpeg
```
## Screenshots
![YT_video_downloader](https://github.com/user-attachments/assets/7344cf3d-2738-4c4a-9557-726d95b797ed)


## Usage

- Run the application by double-clicking on the executable file.
- Enter a YouTube URL in the YouTube URL field.
- Enter a custom filename (without extension) in the Filename field.
- Select a download location by clicking the Browse button.
- Click the Download Video button to start the download.
- A progress bar will show the download progress, and a status label will indicate the current task.
- Once completed, the merged video file will be saved in the chosen location.

## Troubleshooting

- FFmpeg Not Found
If you encounter an error about FFmpeg not being found:

**Windows**: Make sure ffmpeg.exe is in the same directory as your executable or added to your system's PATH.
**macOS/Linux**: Install FFmpeg using your package manager (e.g., brew install ffmpeg on macOS or sudo apt install ffmpeg on Linux).

- Video or Audio Download Fails
This can happen if YouTube's video format changes and pytube is not updated. Ensure that you are using the latest version of pytube:
```bash
pip install --upgrade pytube
```
- Captions Not Downloaded
If captions are not available for a video, they will not be downloaded. This is normal behavior if the video lacks captions in the requested language.
