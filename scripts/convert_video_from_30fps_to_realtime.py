"""
Our videos are generally recorded around 8FPS, however they're saved as though they're 30FPS.
This script uses the JSON files we saved with the timestamps per frame to play the videos at 30FPS but as though
they're in real time by copying the same frame until its time for the next frame.

Note: In order to maintain 30FPS throughout the whole video, we ensure that all within each second after the very first
frame (which occurs at 10:39:03,736), we have 30 frames via repeating frames. Importantly, its each second after 3.736.

Note: to quickly check if things are working, we can just produce the .json file and not process the video
"""
import cv2
import json
import multiprocessing
import os
import time
from copy import deepcopy
from datetime import datetime, timedelta
from typing import List, Tuple

# total_seconds_elapsed = 0  # Global variable to keep track of the number of seconds elapsed since the first frame to maintain 30FPS
# target_second = 1  # The next second we want to reach, incremented by 1 each time we create 30 frames for a given second

created_json_files = []


def parse_timestamp(ts_string):
    return datetime.strptime(ts_string, "%Y-%m-%d %H:%M:%S,%f")


def load_json_data(json_path):
    with open(json_path, 'r') as f:
        return json.load(f)


def extract_frame_data(json_data):
    frames_data = [(parse_timestamp(frame_info[0]), int(frame_number))
                   for frame_number, frame_info in json_data.items()]
    return sorted(frames_data, key=lambda x: x[1])


def calculate_durations(frames_data):
    return [(frames_data[i][0] - frames_data[i-1][0]).total_seconds()
            for i in range(1, len(frames_data))]


def create_video_writer(video_path, fps):
    video = cv2.VideoCapture(video_path)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_filename = f"xrealtime_{video_name}.mp4"
    return cv2.VideoWriter(output_filename, fourcc, fps, (width, height)), video, output_filename


def find_last_frames_index_this_second(
        durations: List[float],
        current_index: int,
        total_seconds_elapsed: int,
        target_second: int
) -> Tuple[int, int, int]:
    """
    Find the index of the last frame in the current second.

    Returns this index.
    """
    for j in range(current_index, len(durations)):
        total_seconds_elapsed += durations[j]
        if total_seconds_elapsed > target_second:
            target_second += 1
            # print(j, total_seconds_elapsed, target_second)
            return j, total_seconds_elapsed, target_second
    return len(durations) - 1, total_seconds_elapsed, target_second


def process_frames(video, frames_data, durations, fps, out=None):
    total_seconds_elapsed = 0
    target_second = 1

    updated_frame_timestamp_json = {}
    current_frame_number = 1
    current_timestamp = frames_data[0][0]

    last_frame_this_second_index_found = False
    index_of_last_frame_this_second = 0

    for i, duration in enumerate(durations):

        # Iterate again through durations, and count the sum, until its over 1
        if last_frame_this_second_index_found == False:
            num_repeated_frames_this_second = 0
            index_of_last_frame_this_second, total_seconds_elapsed, target_second  = find_last_frames_index_this_second(
                durations,
                i,
                total_seconds_elapsed,
                target_second
            )
            last_frame_this_second_index_found = True

        if out:
            ret, frame = video.read()
            if not ret:
                break

            text = f"Frame: {current_frame_number} Timestamp: {current_timestamp.strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]}"
            frame_with_text = deepcopy(frame)
            cv2.putText(frame_with_text, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
            out.write(frame_with_text)

        updated_frame_timestamp_json[str(current_frame_number)] = [current_timestamp.strftime("%Y-%m-%d %H:%M:%S,%f")[:-3], []]
        current_frame_number += 1

        repeat_frames = int(duration * fps) - 1
        num_repeated_frames_this_second += repeat_frames + 1

        if index_of_last_frame_this_second == i:
            # If num_repeated_frames_this_second is less than 30, add the difference to repeat_frames
            repeat_frames += 30 - num_repeated_frames_this_second
            last_frame_this_second_index_found = False  # We're moving onto the next second

        # Repeat the frame for the duration of the frame
        for _ in range(repeat_frames):
            text = f"Frame: {current_frame_number} Timestamp: {current_timestamp.strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]}"
            updated_frame_timestamp_json[str(current_frame_number)] = [current_timestamp.strftime("%Y-%m-%d %H:%M:%S,%f")[:-3], []]
            current_frame_number += 1
            if out:
                # This might make the code a bit slower, but is good to add I think
                frame_with_text = deepcopy(frame)
                cv2.putText(frame_with_text, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
                out.write(frame_with_text)

        current_timestamp += timedelta(seconds=duration)

    return updated_frame_timestamp_json, current_frame_number - 1


def save_json_data(json_data, output_filename):
    with open(output_filename, 'w') as f:
        json.dump(json_data, f, indent=4)


# TODO: I still need to test this function.
def validate_json_data(json_data_file_paths: List[str]):
    for json_file_path in json_data_file_paths:
        with open(json_file_path, 'r') as f:
            json_data = json.load(f)

            # Ensure the first entry exists
            first_entry_timestamp = json_data.get("1", [None])[0]
            if not first_entry_timestamp:
                print(f"File {json_file_path} is invalid: missing first entry.")
                continue

            # Extract the decimal part of the first entry's timestamp
            first_entry_decimal = float(first_entry_timestamp.split(",")[1])

            # Validate every 30th entry
            valid = True
            for i in range(30, len(json_data) + 1, 30):
                entry_timestamp = json_data.get(str(i), [None])[0]
                if not entry_timestamp:
                    print(f"File {json_file_path} is invalid: missing entry {i}.")
                    valid = False
                    break

                entry_decimal = float(entry_timestamp.split(",")[1])
                if entry_decimal >= first_entry_decimal:
                    print(f"File {json_file_path} is invalid: entry {i} decimal part is not less than first entry.")
                    valid = False
                    break

            # Handle the 31st entry case
            if valid and "31" in json_data:
                entry_timestamp_31 = json_data.get("31", [None])[0]
                if entry_timestamp_31:
                    second_part_1 = int(first_entry_timestamp.split(",")[0].split(":")[-1])
                    second_part_31 = int(entry_timestamp_31.split(",")[0].split(":")[-1])
                    if second_part_31 > second_part_1:
                        print(f"File {json_file_path} is invalid: 31st entry's actual second digit is greater than the 1st entry.")
                        valid = False

            if valid:
                print(f"File {json_file_path} is valid.")


def process_video(video_path, json_path, create_video=True):
    start_time = time.time()

    json_data = load_json_data(json_path)
    frames_data = extract_frame_data(json_data)
    durations = calculate_durations(frames_data)

    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)

    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_json_filename = f"realtime_{video_name}.json"

    out = None
    if create_video:
        out, video, output_filename = create_video_writer(video_path, fps)
    else:
        output_filename = "Video not created"

    print(f"Processing {video_name}...")
    updated_frame_timestamp_json, total_frames = process_frames(video, frames_data, durations, fps, out)

    if out:
        out.release()
    video.release()

    save_json_data(updated_frame_timestamp_json, output_json_filename)
    created_json_files.append(output_json_filename)

    end_time = time.time()
    processing_time = end_time - start_time

    print(f"Finished processing {video_name}. Output saved as {output_filename}")
    print(f"New timestamp JSON saved as {output_json_filename}")
    print(f"Processed {total_frames} frames in total.")
    print(f"Processing time: {processing_time:.2f} seconds")
    print(f"Average time per frame: {processing_time / total_frames:.4f} seconds")


def process_video_wrapper(args):
    return process_video(*args)


def main():
    video_json_pairs = {
        r'C:\Users\timf3\PycharmProjects\BallNet\output_marvel-fov-1_time_10_39_10_date_08_06_2024__model_23_05_2024__1608_24_with_bin_out_non_pitch_pixels.avi':
        r'C:\Users\timf3\PycharmProjects\AFLGameSimulation\data\marvel-fov-1_time_02_40_31_date_08_06_2024_1_merged.json',
        r'C:\Users\timf3\PycharmProjects\BallNet\output_marvel-fov-2_time_10_39_13_date_08_06_2024__model_23_05_2024__1608_24_with_bin_out_non_pitch_pixels.avi':
        r'C:\Users\timf3\PycharmProjects\AFLGameSimulation\data\marvel-fov-2_time_02_41_43_date_08_06_2024_1_merged.json',
        r'C:\Users\timf3\PycharmProjects\BallNet\output_marvel-fov-3_time_10_39_15_date_08_06_2024__model_23_05_2024__1608_24_with_bin_out_non_pitch_pixels.avi':
        r'C:\Users\timf3\PycharmProjects\AFLGameSimulation\data\marvel-fov-3_time_02_42_31_date_08_06_2024_1_merged.json',
        r'C:\Users\timf3\PycharmProjects\BallNet\output_marvel-fov-5_time_10_39_03_date_08_06_2024__model_23_05_2024__1608_24_with_bin_out_non_pitch_pixels.avi':
        r'C:\Users\timf3\PycharmProjects\AFLGameSimulation\data\marvel-fov-5_time_02_42_52_date_08_06_2024_1_merged.json',
        r'C:\Users\timf3\PycharmProjects\BallNet\output_marvel-fov-6_time_10_39_15_date_08_06_2024__model_23_05_2024__1608_24_with_bin_out_non_pitch_pixels.avi':
        r'C:\Users\timf3\PycharmProjects\AFLGameSimulation\data\marvel-fov-6_time_02_39_00_date_08_06_2024_1_merged.json',
        r'C:\Users\timf3\PycharmProjects\BallNet\output_marvel-fov-7_time_10_39_15_date_08_06_2024__model_23_05_2024__1608_24_with_bin_out_non_pitch_pixels.avi':
        r'C:\Users\timf3\PycharmProjects\AFLGameSimulation\data\marvel-fov-7_time_02_44_08_date_08_06_2024_1_merged.json',
    }

    create_video = False  # Set this to False if you don't want to create the video file

    # Sequential
    # for video_path, json_path in video_json_pairs.items():
    #     process_video(video_path, json_path, create_video)

    # Parallel
    # Prepare arguments for multiprocessing
    args_list = [(video_path, json_path, create_video) for video_path, json_path in video_json_pairs.items()]

    # Use multiprocessing to process videos concurrently
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        pool.map(process_video_wrapper, args_list)

    # TODO: I still need to test this
    validate_json_data(created_json_files)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()