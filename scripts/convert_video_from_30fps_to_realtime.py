"""
Our videos are generally recorded around 8FPS, however they're saved as though they're 30FPS.
This script uses the JSON files we saved with the timestamps per frame to play the videos at 30FPS but as though
they're in real time by copying the same frame until its time for the next frame.

All hail Claude Sonnet
"""

import json
from datetime import datetime, timedelta
import cv2
import numpy as np
import os

# Function to parse timestamp
def parse_timestamp(ts_string):
    return datetime.strptime(ts_string, "%Y-%m-%d %H:%M:%S,%f")

# Function to process a single video
def process_video(video_path, json_path):
    # Read and parse the JSON file
    with open(json_path, 'r') as f:
        json_data = json.load(f)

    # Extract frame data
    frames_data = []
    for frame_number, frame_info in json_data.items():
        timestamp = parse_timestamp(frame_info[0])
        frames_data.append((timestamp, int(frame_number)))

    # Sort frames by frame number
    frames_data.sort(key=lambda x: x[1])

    # Calculate durations
    durations = []
    for i in range(1, len(frames_data)):
        duration = (frames_data[i][0] - frames_data[i - 1][0]).total_seconds()
        durations.append(duration)

    # Open the video file
    video = cv2.VideoCapture(video_path)

    # Get video properties
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)

    # Create output filename
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_filename = f"realtime_{video_name}.mp4"
    output_json_filename = f"realtime_{video_name}_timestamps.json"

    # Create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))

    # Prepare new JSON data
    new_json_data = {}
    new_frame_number = 1

    # Process each frame
    prev_frame = None
    current_timestamp = frames_data[0][0]
    print(f"Processing {video_name}...")
    for i, duration in enumerate(durations):
        ret, frame = video.read()
        if not ret:
            break

        # Draw frame number and timestamp on the frame
        text = f"Frame: {new_frame_number} Timestamp: {current_timestamp.strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]}"
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # Write the current frame
        out.write(frame)
        new_json_data[str(new_frame_number)] = [current_timestamp.strftime("%Y-%m-%d %H:%M:%S,%f")[:-3], []]
        new_frame_number += 1

        # Calculate how many times to repeat the frame
        repeat_frames = int(duration * fps) - 1

        # Repeat the current frame
        for _ in range(repeat_frames):
            out.write(frame)
            new_json_data[str(new_frame_number)] = [current_timestamp.strftime("%Y-%m-%d %H:%M:%S,%f")[:-3], []]
            new_frame_number += 1

        prev_frame = frame
        current_timestamp += timedelta(seconds=duration)

    # Handle the last frame
    if prev_frame is not None:
        text = f"Frame: {new_frame_number} Timestamp: {current_timestamp.strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]}"
        cv2.putText(prev_frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
        out.write(prev_frame)
        new_json_data[str(new_frame_number)] = [current_timestamp.strftime("%Y-%m-%d %H:%M:%S,%f")[:-3], []]

    # Release everything
    video.release()
    out.release()

    # Write the new JSON file
    with open(output_json_filename, 'w') as f:
        json.dump(new_json_data, f, indent=4)

    print(f"Finished processing {video_name}. Output saved as {output_filename}")
    print(f"New timestamp JSON saved as {output_json_filename}")
    print(f"Processed {new_frame_number} frames in total.")

# Dictionary of video-JSON pairs
video_json_pairs = {
    # r'C:\Users\timf3\PycharmProjects\BallNet\output_marvel-fov-1_time_10_39_10_date_08_06_2024__model_23_05_2024__1608_24_with_bin_out_non_pitch_pixels.avi':
    # r'C:\Users\timf3\PycharmProjects\AFLGameSimulation\data\marvel-fov-1_time_02_40_31_date_08_06_2024_1_merged.json',
    # r'C:\Users\timf3\PycharmProjects\BallNet\output_marvel-fov-2_time_10_39_13_date_08_06_2024__model_23_05_2024__1608_24_with_bin_out_non_pitch_pixels.avi':
    # r'C:\Users\timf3\PycharmProjects\AFLGameSimulation\data\marvel-fov-2_time_02_41_43_date_08_06_2024_1_merged.json',
    # r'C:\Users\timf3\PycharmProjects\BallNet\output_marvel-fov-3_time_10_39_15_date_08_06_2024__model_23_05_2024__1608_24_with_bin_out_non_pitch_pixels.avi':
    # r'C:\Users\timf3\PycharmProjects\AFLGameSimulation\data\marvel-fov-3_time_02_42_31_date_08_06_2024_1_merged.json',
    r'C:\Users\timf3\PycharmProjects\BallNet\output_marvel-fov-5_time_10_39_03_date_08_06_2024__model_23_05_2024__1608_24_with_bin_out_non_pitch_pixels.avi':
    r'C:\Users\timf3\PycharmProjects\AFLGameSimulation\data\marvel-fov-5_time_02_42_52_date_08_06_2024_1_merged.json',
    # r'C:\Users\timf3\PycharmProjects\BallNet\output_marvel-fov-6_time_10_39_15_date_08_06_2024__model_23_05_2024__1608_24_with_bin_out_non_pitch_pixels.avi':
    # r'C:\Users\timf3\PycharmProjects\AFLGameSimulation\data\marvel-fov-6_time_02_39_00_date_08_06_2024_1_merged.json',
    # r'C:\Users\timf3\PycharmProjects\BallNet\output_marvel-fov-7_time_10_39_15_date_08_06_2024__model_23_05_2024__1608_24_with_bin_out_non_pitch_pixels.avi':
    # r'C:\Users\timf3\PycharmProjects\AFLGameSimulation\data\marvel-fov-7_time_02_44_08_date_08_06_2024_1_merged.json',
}

# Process each video-JSON pair
for video_path, json_path in video_json_pairs.items():
    process_video(video_path, json_path)

cv2.destroyAllWindows()
