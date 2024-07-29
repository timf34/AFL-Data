import json
from datetime import datetime, timedelta
import cv2
import os


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
    output_filename = f"realtime_{video_name}.mp4"
    return cv2.VideoWriter(output_filename, fourcc, fps, (width, height)), video, output_filename


def process_frames(video, frames_data, durations, fps, out=None):
    new_json_data = {}
    new_frame_number = 1
    current_timestamp = frames_data[0][0]

    for i, duration in enumerate(durations):
        if out:
            ret, frame = video.read()
            if not ret:
                break

            text = f"Frame: {new_frame_number} Timestamp: {current_timestamp.strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]}"
            cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
            out.write(frame)
        new_json_data[str(new_frame_number)] = [current_timestamp.strftime("%Y-%m-%d %H:%M:%S,%f")[:-3], []]
        new_frame_number += 1

        repeat_frames = int(duration * fps) - 1
        for _ in range(repeat_frames):
            if out:
                out.write(frame)
            new_json_data[str(new_frame_number)] = [current_timestamp.strftime("%Y-%m-%d %H:%M:%S,%f")[:-3], []]
            new_frame_number += 1

        current_timestamp += timedelta(seconds=duration)

    return new_json_data, new_frame_number - 1


def save_json_data(json_data, output_filename):
    with open(output_filename, 'w') as f:
        json.dump(json_data, f, indent=4)


def process_video(video_path, json_path, create_video=True):
    json_data = load_json_data(json_path)
    frames_data = extract_frame_data(json_data)
    durations = calculate_durations(frames_data)

    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)

    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_json_filename = f"temp_realtime_{video_name}_timestamps.json"

    out = None
    if create_video:
        out, video, output_filename = create_video_writer(video_path, fps)
    else:
        output_filename = "Video not created"

    print(f"Processing {video_name}...")
    new_json_data, total_frames = process_frames(video, frames_data, durations, fps, out)

    if out:
        out.release()
    video.release()

    save_json_data(new_json_data, output_json_filename)

    print(f"Finished processing {video_name}. Output saved as {output_filename}")
    print(f"New timestamp JSON saved as {output_json_filename}")
    print(f"Processed {total_frames} frames in total.")


def main():
    video_json_pairs = {
        r'C:\Users\timf3\PycharmProjects\BallNet\output_marvel-fov-5_time_10_39_03_date_08_06_2024__model_23_05_2024__1608_24_with_bin_out_non_pitch_pixels.avi':
        r'C:\Users\timf3\PycharmProjects\AFLGameSimulation\data\marvel-fov-5_time_02_42_52_date_08_06_2024_1_merged.json',
    }

    create_video = False  # Set this to False if you don't want to create the video file

    for video_path, json_path in video_json_pairs.items():
        process_video(video_path, json_path, create_video)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()