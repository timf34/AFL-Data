import json
from datetime import datetime, timedelta
import cv2
import numpy as np
import os
import multiprocessing as mp
from tqdm import tqdm


def parse_timestamp(ts_string):
    return datetime.strptime(ts_string, "%Y-%m-%d %H:%M:%S,%f")


def process_frame(args):
    frame, new_frame_number, current_timestamp, duration, fps = args
    text = f"Frame: {new_frame_number} Timestamp: {current_timestamp.strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]}"
    cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
    repeat_frames = int(duration * fps) - 1
    return frame, repeat_frames, new_frame_number, current_timestamp


def process_video(video_path, json_path):
    with open(json_path, 'r') as f:
        json_data = json.load(f)

    frames_data = [(parse_timestamp(frame_info[0]), int(frame_number))
                   for frame_number, frame_info in json_data.items()]
    frames_data.sort(key=lambda x: x[1])

    durations = [(frames_data[i][0] - frames_data[i - 1][0]).total_seconds()
                 for i in range(1, len(frames_data))]

    video = cv2.VideoCapture(video_path)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)

    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_filename = f"realtime_{video_name}.mp4"
    output_json_filename = f"realtime_{video_name}_timestamps.json"

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))

    new_json_data = {}
    new_frame_number = 1
    current_timestamp = frames_data[0][0]

    num_processes = mp.cpu_count()
    pool = mp.Pool(processes=num_processes)

    frame_buffer = []
    json_buffer = {}

    print(f"Processing {video_name}...")
    results = []
    for i, duration in enumerate(tqdm(durations)):
        ret, frame = video.read()
        if not ret:
            break

        args = (frame, new_frame_number, current_timestamp, duration, fps)
        result = pool.apply_async(process_frame, (args,))
        results.append(result)

        new_frame_number += int(duration * fps)
        current_timestamp += timedelta(seconds=duration)

    pool.close()

    for result in tqdm(results):
        frame, repeat_frames, frame_num, timestamp = result.get()
        frame_buffer.extend([frame] * (repeat_frames + 1))
        for j in range(repeat_frames + 1):
            json_buffer[str(new_frame_number + j)] = [timestamp.strftime("%Y-%m-%d %H:%M:%S,%f")[:-3], []]

        if len(frame_buffer) >= 100:  # Write frames in batches
            for f in frame_buffer:
                out.write(f)
            frame_buffer = []
            new_json_data.update(json_buffer)
            json_buffer = {}

    # Write any remaining frames
    for f in frame_buffer:
        out.write(f)
    new_json_data.update(json_buffer)

    pool.join()

    video.release()
    out.release()

    with open(output_json_filename, 'w') as f:
        json.dump(new_json_data, f)

    print(f"Finished processing {video_name}. Output saved as {output_filename}")
    print(f"New timestamp JSON saved as {output_json_filename}")
    print(f"Processed {new_frame_number} frames in total.")


def main():
    video_json_pairs = {
        r'C:\Users\timf3\PycharmProjects\BallNet\output_marvel-fov-5_time_10_39_03_date_08_06_2024__model_23_05_2024__1608_24_with_bin_out_non_pitch_pixels.avi':
        r'C:\Users\timf3\PycharmProjects\AFLGameSimulation\data\marvel-fov-5_time_02_42_52_date_08_06_2024_1_merged.json',
    }

    for video_path, json_path in video_json_pairs.items():
        process_video(video_path, json_path)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    mp.freeze_support()  # This is necessary for Windows
    main()
