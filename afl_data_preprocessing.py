"""
This script will primarily split the .avi videos into individual frames
"""
import cv2
import math
import os
import subprocess

from moviepy.editor import VideoFileClip
from typing import List

from utils import ensure_directory_exists, find_files_with_ending, png_files_exist, create_directory, mp4_files_exist


VIDEOS_TO_BE_CLIPPED: List[str] = [
    "marvel\\marvel-fov-3\\26_08_2023\\marvel3_time_09_09_04_date_27_08_2023_clipped.mp4"
]
DIRECTORIES_FOR_FRAME_EXTRACTION: [str] = [r'marvel\marvel-fov-3\26_08_2023']


def extract_frames_from_video(file_path: str) -> None:
    """Given a .avi video file path, extract frames using ffmpeg."""

    # Create a directory called "frames"
    file_name_without_extension = os.path.splitext(os.path.basename(file_path))[0]
    file_dir = os.path.dirname(file_path)

    parent_video_name = file_path.split('\\')[-2]
    frames_dir = create_directory(file_dir, directory_name=f'{parent_video_name}{file_name_without_extension}')

    if png_files_exist(frames_dir):
        print(f'Frames already exist in {frames_dir}')
        return

    # Construct the ffmpeg command
    cmd = [
        'ffmpeg',
        '-i', file_path,
        '-vf', 'fps=30/1',
        '-start_number', '0',
        f'{frames_dir}\\frame_%07d.png'
    ]

    # Execute the command via subprocess
    print(cmd)
    subprocess.run(cmd)


def clip_video(video_path: str, output_dir: str, clip_duration: int = 60) -> None:
    """
    This function clips a video into multiple 60 second long clips.
    We use FFmpeg directly to ensure lossless clipping.
    """

    # Check if the output_directory exists, and if not, make it
    ensure_directory_exists(output_dir)

    # Load the video
    video = VideoFileClip(video_path)

    # Calculate the number of clips
    total_duration = video.duration
    num_clips = math.ceil(total_duration / clip_duration)

    # Get the output names
    output_names: List[str] = [output_dir + "\\" + str(i) + ".mp4" for i in range(num_clips)]

    # Clip the video
    for i in range(num_clips):
        # Define the start and end of the clip
        start = i * clip_duration
        end = min((i + 1) * clip_duration, total_duration)

        # Create the subclip
        clip = video.subclip(start, end)

        # Save the clip
        clip_filename = f"{output_names[i]}"
        clip.write_videofile(clip_filename, codec="libx264")
        print(f"Clip {i + 1} saved: {clip_filename}")


def extract_frames_from_all_videos(directories: List[str], file_ending: str = '.mp4') -> None:
    """Given a directory, extract frames from all videos in the directory."""

    for directory in directories:
        avi_files = find_files_with_ending(directory, file_ending=file_ending)
        for avi_file in avi_files:
            extract_frames_from_video(avi_file)


def clip_all_videos_into_sixty_sec_clips(video_paths: List[str]) -> None:
    """
    Given a directory, clip all .avi videos in the directory into 60 second clips.
    Store the new clipped videos in the same directory as the original full video in a folder of the same name.
    """
    for video_file in video_paths:
        # Create directory to store the clipped videos, name it the same as the original video
        file_name_without_extension = os.path.splitext(os.path.basename(video_file))[0]
        file_dir = os.path.dirname(video_file)
        clipped_videos_dir = create_directory(file_dir, directory_name=file_name_without_extension)

        # Check if clipped videos already exist in the directory
        if mp4_files_exist(clipped_videos_dir):
            print(f'Clipped videos already exist in {clipped_videos_dir}. Skipping clipping for {video_file}')
            continue

        # Clip the video
        clip_video(video_file, clipped_videos_dir, 60)


def main():
    clip_all_videos_into_sixty_sec_clips(VIDEOS_TO_BE_CLIPPED)
    extract_frames_from_all_videos(DIRECTORIES_FOR_FRAME_EXTRACTION, file_ending='.mp4')

    # extract_frames_from_video(
    #     file_path=r"C:\Users\timf3\PycharmProjects\AFL-Data\marvel\marvel-fov-6\18_08_2023\clipped\clip_0.mp4"
    # )


if __name__ == '__main__':
    main()
