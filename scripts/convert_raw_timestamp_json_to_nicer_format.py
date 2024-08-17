"""
Converts timestamp json file from this:

{"timestamp": "2024-06-08 10:39:11,644", "level": "INFO", "message": "{'frame': 1}"}
{"timestamp": "2024-06-08 10:39:11,761", "level": "INFO", "message": "{'frame': 2}"}

To this:

{
    "0": "2024-05-12 04:00:04.699000",
    "1": "2024-05-12 04:00:04.979000",


Just copy paste in the raw json above into a temp.json file, then run
"""
import json


def process_json_file(input_file, output_file):
    results = {}
    with open(input_file, 'r') as file:
        for line in file:
            data = json.loads(line)
            # Parse the 'message' string as JSON and extract the frame number
            message_data = json.loads(data['message'].replace("'", "\""))
            frame_number = message_data['frame']
            # Subtract 1 to make frame number zero-indexed
            results[str(frame_number - 1)] = data['timestamp']

    with open(output_file, 'w') as file:
        json.dump(results, file, indent=4)

# Define the paths to the input and output files
input_path = './23_06_2024/unclean_video_timestamp_data/marvel-fov-1_time_02_36_49_date_23_06_2024_1.json'
output_path = 'output.json'

# Call the function with the hardcoded paths
process_json_file(input_path, output_path)

print("JSON processing complete. Output saved to:", output_path)
