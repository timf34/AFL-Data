import os
import cv2

from sagemaker_utils import *

VIDEO: str = "marvel/marvel-fov-3/20_08_2023/time_04_09_06_date_20_08_2023_.avi"

def extract_frames_from_video_cv2(file_path: str, fps: int = 30) -> None:
    """Given a video file path, extract frames using OpenCV (imageio is too slow for this)."""

    # Create a directory called "frames"
    file_name_without_extension = os.path.splitext(os.path.basename(file_path))[0]
    file_dir = os.path.dirname(file_path)

    parent_video_name = file_path.split(os.sep)[-2]
    frames_dir = create_directory(file_dir, directory_name=f'{parent_video_name}{file_name_without_extension}')

    # Use OpenCV to read the video and save frames
    cap = cv2.VideoCapture(file_path)
    video_fps = int(cap.get(cv2.CAP_PROP_FPS))

    # We'll only save every nth frame to match the desired FPS (fps parameter)
    n = int(video_fps / fps)

    frame_num = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_num % n == 0:
            frame_file_path = os.path.join(frames_dir, f"frame_{frame_num // n:07d}.png")
            cv2.imwrite(frame_file_path, frame)
        frame_num += 1

    cap.release()
    print(f"Frames extracted to {frames_dir}")


extract_frames_from_video_cv2(VIDEO)