"""
Our videos are generally recorded around 8FPS, however they're saved as though they're 30FPS.
This script uses the JSON files we saved with the timestamps per frame to play the videos at 30FPS but as though
they're in real time by copying the same frame until its time for the next frame.

All hail Claude Sonnet
"""

import json
from datetime import datetime
import cv2
import numpy as np


# Function to parse timestamp
def parse_timestamp(ts_string):
    return datetime.strptime(ts_string, "%Y-%m-%d %H:%M:%S,%f")


# Read and parse the JSON file
with open(r'C:\Users\timf3\PycharmProjects\AFLGameSimulation\data\marvel-fov-1_time_02_40_31_date_08_06_2024_1_merged.json', 'r') as f:

    json_data = json.load(f)

# Extract frame data
frames_data = []
for frame_number, frame_info in json_data.items():
    timestamp = parse_timestamp(frame_info[0])
    frames_data.append((timestamp, int(frame_number)))

# Sort frames by frame number
frames_data.sort(key=lambda x: x[1])

# Sort frames by frame number
frames_data.sort(key=lambda x: x[1])

# Calculate durations
durations = []
for i in range(1, len(frames_data)):
    duration = (frames_data[i][0] - frames_data[i - 1][0]).total_seconds()
    durations.append(duration)

# Open the video file
video = cv2.VideoCapture(r'C:\Users\timf3\PycharmProjects\BallNet\output_marvel-fov-1_time_10_39_10_date_08_06_2024__model_23_05_2024__1608_24_with_bin_out_non_pitch_pixels.avi')

# Get video properties
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = video.get(cv2.CAP_PROP_FPS)

# Create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_video.mp4', fourcc, fps, (width, height))

# Process each frame
prev_frame = None
print("Processing frames...")
for i, duration in enumerate(durations):
    ret, frame = video.read()
    if not ret:
        break

    # Write the current frame
    out.write(frame)

    # Calculate how many times to repeat the frame
    repeat_frames = int(duration * fps) - 1

    # Repeat the current frame
    for _ in range(repeat_frames):
        out.write(frame)

    prev_frame = frame

# Handle the last frame
if prev_frame is not None:
    out.write(prev_frame)

# Release everything
video.release()
out.release()
cv2.destroyAllWindows()