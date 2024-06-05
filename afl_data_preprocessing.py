"""
This script will primarily split the .avi videos into individual frames
"""
import math
import os
import subprocess

from moviepy.editor import VideoFileClip
from typing import List

from utils import ensure_directory_exists, find_files_with_ending, png_files_exist, create_directory, mp4_files_exist

CLIP_LENGTH_SECONDS: int = 60
USE_JPG: bool = False  # We get blocky images by default... there might be a better way to do this, I'll just need to look into it another time

VIDEOS_TO_BE_CLIPPED: List[str] = [
    # "marvel\\marvel-fov-3\\26_08_2023\\marvel3_time_09_09_04_date_27_08_2023_clipped.mp4"
    # "marvel\\marvel-fov-4\\26_08_23\\marvel4_time_09_09_03_date_27_08_2023_.avi"
    # "marvel\\marvel-fov-8\\18_08_2023\\marvel8_time_10_24_04_date_19_08_2023_.avi",
    # "marvel\\marvel-fov-1\\18_08_2023\\marvel1_time_10_24_03_date_19_08_2023_.avi",
    # "marvel\\marvel-fov-2\\18_08_2023\\marvel2_time_10_24_03_date_19_08_2023_.avi",
    # "marvel\\marvel-fov-3\\18_08_2023\\marvel3_time_10_24_03_date_19_08_2023_.avi"
    # "marvel\\marvel-fov-2\\13_04_2024\\marvel2_time_07_34_03_date_13_04_2024_.mkv",
    # "marvel\\marvel-fov-1\\13_04_2024\\marvel1_time_07_34_03_date_13_04_2024_.mkv",
    # "marvel\\marvel-fov-5\\11_05_2024\\marvel-fov-5_time_04_00_05_date_12_05_2024_.avi"
    # "marvel\\marvel-fov-6\\19_05_2024\\marvel-fov-6_time_04_21_07_date_19_05_2024_.avi"
    # "marvel\\marvel-fov-7\\19_05_2024\\marvel-fov-7_time_04_42_10_date_19_05_2024_.avi"
    # "marvel\\marvel-fov-6\\21_04_2024\\marvel6_time_09_30_11_date_21_04_2024_.avi"
    "marvel\\marvel-fov-5\\27_08_2023\\marvel5_time_09_09_04_date_27_08_2023_.avi"
]

VIDEOS_FOR_FRAME_EXTRACTION: List[str] = [
    # r"C:\Users\timf3\PycharmProjects\AFL-Data\marvel\marvel-fov-2\13_04_2024\marvel2_time_07_34_03_date_13_04_2024_\4.mp4",
    # r"C:\Users\timf3\PycharmProjects\AFL-Data\marvel\marvel-fov-2\13_04_2024\marvel2_time_07_34_03_date_13_04_2024_\5.mp4",
    # r"C:\Users\timf3\PycharmProjects\AFL-Data\marvel\marvel-fov-2\13_04_2024\marvel2_time_07_34_03_date_13_04_2024_\6.mp4",
    # r"C:\Users\timf3\PycharmProjects\AFL-Data\marvel\marvel-fov-2\13_04_2024\marvel2_time_07_34_03_date_13_04_2024_\7.mp4",
    # r"C:\Users\timf3\PycharmProjects\AFL-Data\marvel\marvel-fov-2\13_04_2024\marvel2_time_07_34_03_date_13_04_2024_\8.mp4",
    # r"C:\Users\timf3\PycharmProjects\AFL-Data\marvel\marvel-fov-1\13_04_2024\marvel1_time_07_34_03_date_13_04_2024_\4.mp4",
    # r"C:\Users\timf3\PycharmProjects\AFL-Data\marvel\marvel-fov-1\13_04_2024\marvel1_time_07_34_03_date_13_04_2024_\5.mp4",
    # r"C:\Users\timf3\PycharmProjects\AFL-Data\marvel\marvel-fov-1\13_04_2024\marvel1_time_07_34_03_date_13_04_2024_\6.mp4",
    # r"C:\Users\timf3\PycharmProjects\AFL-Data\marvel\marvel-fov-1\13_04_2024\marvel1_time_07_34_03_date_13_04_2024_\7.mp4",
    # r"C:\Users\timf3\PycharmProjects\AFL-Data\marvel\marvel-fov-1\13_04_2024\marvel1_time_07_34_03_date_13_04_2024_\8.mp4"
    # r"C:\Users\timf3\PycharmProjects\AFL-Data\marvel\marvel-fov-5\27_08_2023\marvel5_time_09_09_04_date_27_08_2023_\0.mp4",
    # r"C:\Users\timf3\PycharmProjects\AFL-Data\marvel\marvel-fov-5\27_08_2023\marvel5_time_09_09_04_date_27_08_2023_\1.mp4",
    # r"C:\Users\timf3\PycharmProjects\AFL-Data\marvel\marvel-fov-5\27_08_2023\marvel5_time_09_09_04_date_27_08_2023_\2.mp4",
    # r"C:\Users\timf3\PycharmProjects\AFL-Data\marvel\marvel-fov-5\27_08_2023\marvel5_time_09_09_04_date_27_08_2023_\3.mp4",
    # r"C:\Users\timf3\PycharmProjects\AFL-Data\marvel\marvel-fov-5\27_08_2023\marvel5_time_09_09_04_date_27_08_2023_\5.mp4",
    r"C:\Users\timf3\PycharmProjects\AFL-Data\marvel\marvel-fov-5\27_08_2023\marvel5_time_09_09_04_date_27_08_2023_\7.mp4",
]

DIRECTORIES_FOR_FRAME_EXTRACTION: [str] = [
    # r'marvel\marvel-fov-3\26_08_2023\marvel3_time_09_09_04_date_27_08_2023_clipped',
    # r'marvel\marvel-fov-3\26_08_2023\marvel3_time_09_09_04_date_27_08_2023_',
    # r'marvel\marvel-fov-4\26_08_23\marvel4_time_09_09_03_date_27_08_2023_'
    # r"marvel\marvel-fov-6\18_08_2023\marvel6_time_10_24_03_date_19_08_2023_",
    # r"marvel\marvel-fov-1\18_08_2023\marvel1_time_10_24_03_date_19_08_2023_",
    # r"marvel\marvel-fov-3\18_08_2023\marvel3_time_10_24_03_date_19_08_2023_",
    # r"marvel\marvel-fov-8\18_08_2023\marvel8_time_10_24_04_date_19_08_2023_"
    r"marvel\marvel-fov-5\11_05_2024\marvel-fov-5_time_04_00_05_date_12_05_2024_"
]


def extract_frames_from_video(file_path: str) -> None:
    """Given a .avi video file path, extract frames using ffmpeg."""

    # Ensure file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File does not exist: {file_path}")

    # Create a directory called "frames"
    file_name_without_extension = os.path.splitext(os.path.basename(file_path))[0]
    file_dir = os.path.dirname(file_path)

    parent_video_name = file_path.split('\\')[-2]
    frames_dir = create_directory(file_dir, directory_name=f'{parent_video_name}{file_name_without_extension}')

    if png_files_exist(frames_dir):
        print(f'Frames already exist in {frames_dir}')
        return

    if USE_JPG is True:
        image_extension = ".jpg"
    else:
        image_extension = ".png"

    # Construct the ffmpeg command
    cmd = [
        'ffmpeg',
        '-i', file_path,
        '-vf', 'fps=30/1',
        '-start_number', '0',
        f'{frames_dir}\\frame_%07d{image_extension}'
    ]

    # Execute the command via subprocess
    print(cmd)
    subprocess.run(cmd)


def clip_video(video_path: str, output_dir: str, clip_duration_seconds: int = 60) -> None:
    """
    This function clips a video into multiple 60 second long clips.
    We use FFmpeg directly to ensure lossless clipping.
    """
    # Ensure video path exists
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"File does not exist: {video_path}")

    # Check if the output_directory exists, and if not, make it
    ensure_directory_exists(output_dir)

    # Load the video
    video = VideoFileClip(video_path)

    # Calculate the number of clips
    total_duration = video.duration
    num_clips = math.ceil(total_duration / clip_duration_seconds)

    # Get the output names
    output_names: List[str] = [output_dir + "\\" + str(i) + ".mp4" for i in range(num_clips)]

    # Clip the video
    for i in range(num_clips):
        # Define the start and end of the clip
        start = i * clip_duration_seconds
        end = min((i + 1) * clip_duration_seconds, total_duration)

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


def extract_frames_from_video_paths(video_paths: List[str]) -> None:
    """Given a list of video paths, extract frames from all videos in the list."""
    for video_path in video_paths:
        extract_frames_from_video(video_path)


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
        clip_video(video_file, clipped_videos_dir, CLIP_LENGTH_SECONDS)


def main():

    # First clip a long video into 1 min clips
    # clip_all_videos_into_sixty_sec_clips(VIDEOS_TO_BE_CLIPPED)

    # Then we extract the frames from these 1 minute clips
    # extract_frames_from_all_videos(DIRECTORIES_FOR_FRAME_EXTRACTION, file_ending='.mp4')
    extract_frames_from_video_paths(VIDEOS_FOR_FRAME_EXTRACTION)

    # extract_frames_from_video(
    #     file_path=r"C:\Users\timf3\PycharmProjects\AFL-Data\marvel\marvel-fov-5\11_05_2024\marvel-fov-5_time_04_00_05_date_12_05_2024_\0.mp4"
    # )


if __name__ == '__main__':
    main()
