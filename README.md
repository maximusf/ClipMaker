# Clip Maker

Clip Maker is a simple tool that splits your MP4 videos into smaller clips, perfect for sharing on Instagram. It works on Windows, Mac, and Linux.

## What You Need

- **Python**: A programming language. Don't worry, you don't need to know how to code!
- **FFmpeg**: A tool that helps process videos.
- **VS Code**: A program to run the script (optional, but recommended).

## Getting Started

### Step 1: Install Python

1. Go to [python.org](https://www.python.org/downloads/).
2. Download and install Python. Make sure to check the box that says "Add Python to PATH" during installation.

### Step 2: Install VS Code (Optional)

1. Download and install Visual Studio Code from [code.visualstudio.com](https://code.visualstudio.com/).
2. Open VS Code.

### Step 3: Install Required Tools

1. Open a terminal:
   - **Windows**: Press `Win + R`, type `cmd`, and press Enter.
   - **Mac/Linux**: Open Terminal from Applications or use `Ctrl + Alt + T`.

2. Type the following command and press Enter:
   ```bash
   pip install ffmpeg-python
   ```

### Step 4: Install FFmpeg

1. Download FFmpeg from [FFmpeg Builds](https://github.com/BtbN/FFmpeg-Builds/releases).
2. Extract the downloaded file to a folder, e.g., `C:\ffmpeg`.
3. Add FFmpeg to your system PATH:
   - **Windows**: 
     - Search for "Environment Variables" in the Start menu.
     - Click "Edit the system environment variables".
     - Click "Environment Variables".
     - Find "Path" in the list, click "Edit", and add `C:\ffmpeg\bin`.
   - **Mac/Linux**: Open Terminal and type:
     ```bash
     echo 'export PATH="/path/to/ffmpeg/bin:$PATH"' >> ~/.bash_profile
     source ~/.bash_profile
     ```

## How to Use Clip Maker

1. **Place your MP4 videos** in the same folder as the `desktop_video_splitter.py` script.

2. **Open a terminal** and navigate to the script's folder:
   ```bash
   cd path/to/your/script/folder
   ```

3. **Run the script**:
   ```bash
   python desktop_video_splitter.py
   ```

4. **Follow the instructions** on the screen:
   - Type the number of the video you want to split.
   - Type `cancel` if you change your mind.
   - Type `reload` to refresh the video list.
   - Type `done` when you're finished selecting videos.

5. **Check the output**:
   - The clips will be saved in a folder called `split_videos`.
   - Each video will have its own subfolder.

## Troubleshooting

- If you see an error about FFmpeg, make sure it's installed and added to your PATH.
- If the script is slow, it might be because your computer doesn't support hardware acceleration.

## Need Help?

If you get stuck, feel free to search online for help with Python, FFmpeg, or using the terminal. There are lots of tutorials and forums where you can find answers!
