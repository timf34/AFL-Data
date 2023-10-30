import cv2
from sagemaker_utils import *

from typing import List, Dict

# Folder path
XML_FILE: str = r"C:\Users\timf3\PycharmProjects\AFL-Data\marvel\afl-preprocessed\train\annotations\marvel_1_time_04_09_04_date_20_08_2023_0.xml"
FOLDER: str = "../test-marvel/marvel_3_time_04_09_06_date_20_08_2023_0"
VIDEO_PATH: str = "../test-marvel/marvel_3_time_04_09_06_date_20_08_2023_0.mp4"


def extract_frames_from_video_cv2(file_path: str, fps: int = 30) -> None:
    """Given a video file path, extract frames using OpenCV (imageio is too slow for this)."""

    # Create a directory called "frames"
    file_name_without_extension = os.path.splitext(os.path.basename(file_path))[0]
    file_dir = os.path.dirname(file_path)

    frames_dir = create_directory(file_dir, directory_name=f'{file_name_without_extension}')

    if count_files_with_extension(frames_dir, '.png') > 1780:
        print(f'Frames already exist in {frames_dir}')
        return

    # Ensure the video path exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'Video file not found at {file_path}')

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




def main():
    extract_frames_from_video_cv2(VIDEO_PATH)

    frame_nums: List[int] = get_frames_containing_ball(XML_FILE)
    file_names: List[str] = [get_frame_name_from_frame_number(frame_num) for frame_num in frame_nums]


    # List all the files with extension png in the folder
    files: List[str] = [f for f in os.listdir(FOLDER) if os.path.isfile(os.path.join(FOLDER, f)) and f.endswith('.png')]
    print(files)

    # Remove the files that are not in the list
    for file in files:
        if file not in file_names:
            os.remove(os.path.join(FOLDER, file))

if __name__ == '__main__':
    main()
