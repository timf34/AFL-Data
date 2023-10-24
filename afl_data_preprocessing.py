"""
This script will primarily split the .avi videos into individual frames
"""
import cv2
import imageio
import os
import subprocess
from typing import List

from utils import ensure_directory_exists, find_files_with_ending, png_files_exist, create_directory, mp4_files_exist

AFL_DATA_DIR: str = r'marvel/marvel-fov-6'


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


def clip_video(video, output_dir: str, clip_length: int) -> None:
    """
    This function clips a video into multiple 60 second long clips.
    We use FFmpeg directly to ensure lossless clipping.
    """

    # Check if the output_directory exists, and if not, make it
    ensure_directory_exists(output_dir)

    # Load the video and get its length
    cv2_video = cv2.VideoCapture(video)
    video_length: int = int(cv2_video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps: int = int(cv2_video.get(cv2.CAP_PROP_FPS))

    # Get the number of clips we need to make
    num_clips: int = (video_length // fps) // clip_length

    # Get the remainder
    remainder: int = video_length % clip_length

    # Get the start and end times for each clip
    start_times: List[int] = [i * clip_length for i in range(num_clips)]

    # If there is a remainder, add it to the end of the list
    if remainder > 0:
        start_times.append(num_clips * clip_length)

    # Get the end times
    end_times: List[int] = [i + clip_length for i in start_times]

    # Get the output names
    output_names: List[str] = [output_dir + "\\" + str(i) + ".mp4" for i in range(len(start_times))]

    # Clip the video
    for i in range(len(start_times)):
        print(f"Clipping video {video} from {start_times[i]} to {end_times[i]}")

        # Craft the FFmpeg command for lossless clipping
        cmd = [
            'ffmpeg',
            '-i', video,
            '-ss', str(start_times[i]),
            '-t', str(clip_length),
            '-c:v', 'copy',
            '-an',  # This excludes the audio. If you want to include audio, you can remove this.
            output_names[i]
        ]

        subprocess.run(cmd)

        print(f"Finished clipping video {video} from {start_times[i]} to {end_times[i]}")


def clip_video_imageio(video_path: str, output_dir: str, clip_length: int = 60) -> None:
    """
        Clip a video into multiple segments of the given length using imageio.

        Parameters:
        - video_path: Path to the video file.
        - output_dir: Directory to store the clipped videos.
        - clip_length: Duration of each clip in seconds (default is 60 seconds).
        """
    reader = imageio.get_reader(video_path)
    fps = reader.get_meta_data()['fps']

    # Calculate the number of frames needed for the specified clip length
    frames_per_clip = int(clip_length * fps)

    # Create the output directory if it doesn't exist
    ensure_directory_exists(output_dir)

    num_frames = len(reader)

    for start_frame in range(0, num_frames, frames_per_clip):
        end_frame = min(start_frame + frames_per_clip, num_frames)

        # Define the output file name
        output_file = os.path.join(output_dir, f"clip_{start_frame // frames_per_clip}.mp4")

        # Check if this clip is too short (ignores the remainder)
        if end_frame - start_frame < clip_length * 0.5 * fps:
            break

        print(f"Clipping video {video_path} from frame {start_frame} to {end_frame}")

        # Write the segment to a new file
        writer = imageio.get_writer(output_file, fps=fps, macro_block_size=1)
        for frame in range(start_frame, end_frame):
            writer.append_data(reader.get_data(frame))
        writer.close()

        print(f"Finished clipping video segment {output_file}")


def extract_frames_from_all_videos(directory: str, file_ending: str = '.avi') -> None:
    """Given a directory, extract frames from all .avi videos in the directory."""
    avi_files = find_files_with_ending(directory, file_ending=file_ending)
    for avi_file in avi_files:
        extract_frames_from_video(avi_file)


def clip_all_videos_into_sixty_sec_clips(directory: str, file_ending: str = '.avi') -> None:
    """
    Given a directory, clip all .avi videos in the directory into 60 second clips.
    Store the new clipped videos in the same directory as the original full video in a folder of the same name.
    """
    # Find all .avi files in the directory
    avi_files = find_files_with_ending(directory, file_ending=file_ending)

    for avi_file in avi_files:
        # Create directory to store the clipped videos, name it the same as the original video
        file_name_without_extension = os.path.splitext(os.path.basename(avi_file))[0]
        file_dir = os.path.dirname(avi_file)
        clipped_videos_dir = create_directory(file_dir, directory_name=file_name_without_extension)

        # Check if clipped videos already exist in the directory
        if mp4_files_exist(clipped_videos_dir):
            print(f'Clipped videos already exist in {clipped_videos_dir}. Skipping clipping for {avi_file}')
            continue

        # Clip the video
        clip_video(avi_file, clipped_videos_dir, 60)



def main():
    # extract_frames_from_all_videos(AFL_DATA_DIR, file_ending='.mp4')
    # clip_all_videos_into_sixty_sec_clips(AFL_DATA_DIR)
    clip_video_imageio(
        video_path=r"C:\Users\timf3\PycharmProjects\AFL-Data\marvel\marvel-fov-6\18_08_2023\marvel_6_time_10_24_03_date_19_08_2023_.avi",
        output_dir=r"C:\Users\timf3\PycharmProjects\AFL-Data\marvel\marvel-fov-6\18_08_2023\clipped",
        clip_length=60
    )


if __name__ == '__main__':
    main()
