# desktop_video_splitter.py
# Copyright 2024 maximusf

# This script splits MP4 video files into Instagram-compatible segments.
# It uses FFmpeg for video processing and supports hardware acceleration for faster encoding.

from typing import Union, List, Optional
from pathlib import Path
import ffmpeg
import os
import time
import shutil

def display_logo() -> None:
    """Display the ASCII art logo for the application."""
    logo = """
 ________  ___       ___  ________        _____ ______   ________  ___  __    _______   ________     
|\\   ____\\|\\  \\     |\\  \\|\\   __  \\      |\\   _ \\  _   \\|\\   __  \\|\\  \\|\\  \\ |\\  ___ \\ |\\   __  \\    
\\ \\  \\___|\\ \\  \\    \\ \\  \\ \\  \\|\\  \\     \\ \\  \\\\\\__\\ \\  \\ \\  \\|\\  \\ \\  \\/  /|\\ \\   __/|\\ \\  \\|\\  \\   
 \\ \\  \\    \\ \\  \\    \\ \\  \\ \\   ____\\     \\ \\  \\\\|__| \\  \\ \\   __  \\ \\   ___  \\ \\  \\_|/_\\ \\   _  _\\  
  \\ \\  \\____\\ \\  \\____\\ \\  \\ \\  \\___|      \\ \\  \\    \\ \\  \\ \\  \\ \\  \\ \\  \\\\ \\  \\ \\  \\_|\\ \\ \\  \\\\  \\| 
   \\ \\_______\\ \\_______\\ \\__\\ \\__\\          \\ \\__\\    \\ \\__\\ \\__\\ \\__\\ \\__\\\\ \\__\\ \\_______\\ \\__\\\\ _\\ 
    \\|_______|\\|_______|\\|__|\\|__|           \\|__|     \\|__|\\|__|\\|__|\\|__| \\|__|\\|_______|\\|__|\\|__|
                                                                                                     
                                Instagram Video Splitter - v1.0
                                Created by Max
    """
    print(logo)
    print("-" * 100 + "\n")

def cleanup_output_directory(directory: Path) -> None:
    """
    Clean up the output directory by removing all contents.
    
    Args:
        directory: Directory to clean up
    """
    if directory.exists():
        print("\nCleaning up previous output directory...")
        try:
            shutil.rmtree(directory)
            print("Previous output directory cleaned successfully.")
        except Exception as e:
            print(f"Error cleaning directory: {str(e)}")
    
    # Recreate the empty directory
    directory.mkdir(parents=True, exist_ok=True)
    print("Created fresh output directory.")

def get_mp4_files(directory: Path) -> List[Path]:
    """
    Get all MP4 files in the specified directory.
    
    Args:
        directory: Directory to search for MP4 files
    
    Returns:
        List of paths to MP4 files
    """
    return sorted(directory.glob("*.mp4"))

def select_videos(videos: List[Path]) -> List[Path]:
    """
    Let user select multiple videos from the list.
    
    Args:
        videos: List of video paths to choose from
    
    Returns:
        List of selected video paths
    """
    if not videos:
        print("\nNo MP4 files found in the current directory!")
        return []
        
    print("\nAvailable videos:")
    for i, video in enumerate(videos, 1):
        print(f"{i}. {video.name}")
    
    selected_videos = []
    while True:
        choice = input("\nEnter the number of the video to process, 'cancel' to remove last selection, 'reload' to refresh the list, or 'done' to finish: ").strip()
        if choice.lower() == 'done':
            break
        elif choice.lower() == 'cancel':
            if selected_videos:
                removed_video = selected_videos.pop()
                print(f"Removed {removed_video.name} from the processing list.")
            else:
                print("No videos to remove.")
        elif choice.lower() == 'reload':
            videos = get_mp4_files(Path(__file__).parent)
            print("\nReloaded video list:")
            for i, video in enumerate(videos, 1):
                print(f"{i}. {video.name}")
        else:
            try:
                index = int(choice) - 1
                if 0 <= index < len(videos):
                    if videos[index] in selected_videos:
                        print("This video is already selected. Please choose another or type 'done'.")
                    else:
                        selected_videos.append(videos[index])
                        print(f"Added {videos[index].name} to the processing list.")
                else:
                    print("Invalid selection. Please enter a number from the list.")
            except ValueError:
                print("Please enter a valid number, 'cancel', 'reload', or 'done'.")
    
    return selected_videos

def split_video(
    input_path: Union[str, Path], 
    output_dir: Union[str, Path], 
    segment_length: int = 60,
    target_size_mb: int = 24
) -> List[Path]:
    """
    Splits an MP4 video file into Instagram-compatible segments with hardware acceleration.

    Args:
        input_path: Path to the input video file
        output_dir: Directory where split videos will be saved
        segment_length: Length of each segment in seconds (max 60 for Instagram)
        target_size_mb: Target size in MB for each segment (max 25 for Instagram)
    """
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Video file not found: {input_path}")

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_files: List[Path] = []

    try:
        # Get video duration
        probe = ffmpeg.probe(str(input_path))
        duration = float(probe['format']['duration'])
        
        # Calculate number of segments
        num_segments = int(duration // segment_length)
        if duration % segment_length > 0:
            num_segments += 1

        print(f"\nProcessing {num_segments} segments for {input_path.name}...")
        
        # Split the video
        for i in range(num_segments):
            start_time = i * segment_length
            output_path = output_dir / f"{input_path.stem}_segment_{i+1:03d}.mp4"
            
            print(f"\nProcessing segment {i+1}/{num_segments}")
            start_process = time.time()
            
            # Use ffmpeg with hardware acceleration and scaled resolution
            (
                ffmpeg
                .input(str(input_path), ss=start_time, t=segment_length)
                .output(str(output_path),
                    # Video settings with hardware acceleration
                    vcodec='h264_nvenc' if ffmpeg.probe(str(input_path))['streams'][2]['codec_name'] == 'hevc' else 'libx264',
                    video_bitrate=f'{target_size_mb/2}M',
                    maxrate=f'{target_size_mb}M',
                    bufsize=f'{target_size_mb*2}M',
                    # Scale down to 1080p
                    vf='scale=-1:1080',
                    # Audio settings
                    acodec='aac',
                    audio_bitrate='128k',
                    # General settings
                    f='mp4',
                    preset='fast'
                )
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
            
            process_time = time.time() - start_process
            print(f"Segment {i+1} completed in {process_time:.2f} seconds")
            
            output_files.append(output_path)

        return output_files

    except ffmpeg.Error as e:
        print(f"FFmpeg Error Details: {e.stderr.decode()}")
        raise RuntimeError(f"FFmpeg error: {str(e.stderr.decode())}")
    except Exception as e:
        print(f"General Error Details: {str(e)}")
        raise RuntimeError(f"Error processing video: {str(e)}")

def main() -> None:
    """Main function to process the video file."""
    # Display the logo
    display_logo()
    
    # Get the root directory path
    root_path = Path(__file__).parent
    
    # Create and clean output directory
    output_dir = root_path / "split_videos"
    cleanup_output_directory(output_dir)
    
    while True:
        # Get list of MP4 files
        videos = get_mp4_files(root_path)
        
        # Let user select videos
        selected_videos = select_videos(videos)
        if not selected_videos:
            print("No videos selected. Exiting...")
            return
        
        try:
            for video in selected_videos:
                video_output_dir = output_dir / video.stem
                start_time = time.time()
                output_files = split_video(video, video_output_dir)
                total_time = time.time() - start_time
                
                print(f"\nSuccessfully split {video.name} into {len(output_files)} segments")
                print(f"Total processing time: {total_time:.2f} seconds")
                print("\nOutput files:")
                for file in output_files:
                    print(f"- {file}")
            
            # Ask if the user wants to process another file
            another = input("\nDo you want to process another file? (yes/no): ").strip().lower()
            if another != 'yes':
                print("Exiting Clip Maker. Goodbye!")
                break
            
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()