"""
Note: this is copied here from AFLGameSimulations

This script is to merge the simplified tensorrt json file (frame_number:datetime) with the detections
json file (frame_number:detection) to create a new json file with the following format:

(frame_number: (datetime, detection))
"""


import json
from datetime import datetime


# TODO: this seems to move detections forward a frame which I think is wrong... unless I'm rectifying a mistake I
#  made earlier. Let's continue for now, but I have a feeling this is a bug somewhere...

def merge_json_files(datetime_file, detections_file, output_file_base):
    # Load the JSON files
    with open(datetime_file, 'r') as f:
        datetime_data = json.load(f)

    with open(detections_file, 'r') as f:
        detections_data = json.load(f)

    # Merge the JSON files
    merged_data = {}
    for frame_number in datetime_data.keys():
        datetime_value = datetime_data[frame_number]
        adjusted_frame_number = int(frame_number) - 1  # The detections data is indexed from 0
        detections_value = detections_data.get(str(adjusted_frame_number), [])
        merged_data[frame_number] = (datetime_value, detections_value)

    # Generate a unique output file name with a timestamp
    output_file = f"{output_file_base}_merged.json"

    # Save the merged JSON to a new file
    with open(output_file, 'w') as f:
        json.dump(merged_data, f, indent=4)

    print(f"Merged JSON file created successfully: {output_file}")

# Dictionary mapping datetime JSON files to detections JSON files
json_file_mappings = {
    "./23_06_2024/processed_video_timestamp_data/marvel-fov-1_time_02_36_49_date_23_06_2024_1.json":
        "./23_06_2024/detections_data/trt_output_marvel-fov-1_time_04_00_04_date_23_06_2024__model_23_05_2024_1608_24_windows_threshold_90_with_bin_out_non_pitch_pixels_detections.json",
    "./23_06_2024/processed_video_timestamp_data/marvel-fov-2_time_02_37_48_date_23_06_2024_1.json":
        "./23_06_2024/detections_data/trt_output_marvel-fov-2_time_04_00_03_date_23_06_2024__model_23_05_2024_1608_24_windows_threshold_90_with_bin_out_non_pitch_pixels_detections.json",
    "./23_06_2024/processed_video_timestamp_data/marvel-fov-3_time_02_38_13_date_23_06_2024_1.json":
        "./23_06_2024/detections_data/trt_output_marvel-fov-3_time_04_00_04_date_23_06_2024__model_23_05_2024_1608_24_windows_threshold_90_with_bin_out_non_pitch_pixels_detections.json",
    "./23_06_2024/processed_video_timestamp_data/marvel-fov-5_time_02_42_45_date_23_06_2024_1.json":
        "./23_06_2024/detections_data/trt_output_marvel-fov-5_time_04_00_05_date_23_06_2024__model_23_05_2024_1608_24_windows_threshold_90_with_bin_out_non_pitch_pixels_detections.json",
    "./23_06_2024/processed_video_timestamp_data/marvel-fov-6_time_02_43_13_date_23_06_2024_1.json":
        "./23_06_2024/detections_data/trt_output_marvel-fov-6_time_04_00_04_date_23_06_2024__model_23_05_2024_1608_24_windows_threshold_90_with_bin_out_non_pitch_pixels_detections.json",
    "./23_06_2024/processed_video_timestamp_data/marvel-fov-7_time_02_43_51_date_23_06_2024_1.json":
        "./23_06_2024/detections_data/trt_output_marvel-fov-7_time_04_00_04_date_23_06_2024__model_23_05_2024_1608_24_windows_threshold_90_with_bin_out_non_pitch_pixels_detections.json",
    "./23_06_2024/processed_video_timestamp_data/marvel-fov-9_time_02_44_10_date_23_06_2024_1.json":
        "./23_06_2024/detections_data/trt_output_marvel-fov-9_time_04_00_03_date_23_06_2024__model_23_05_2024_1608_24_windows_threshold_90_with_bin_out_non_pitch_pixels_detections.json",
    "./23_06_2024/processed_video_timestamp_data/marvel-fov-10_time_02_45_08_date_23_06_2024_1.json":
        "./23_06_2024/detections_data/trt_output_marvel-fov-10_time_04_00_04_date_23_06_2024__model_23_05_2024_1608_24_windows_threshold_90_with_bin_out_non_pitch_pixels_detections.json",
}

# TODO: this is saving things to "processed_video_Timestamp" and I'm needing to move them manually thereafter

# Process each pair of files
for datetime_file, detections_file in json_file_mappings.items():
    output_file_base = datetime_file.replace("frame_timestamp_map", "merged_frame_data")
    merge_json_files(datetime_file, detections_file, output_file_base)
