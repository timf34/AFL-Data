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
import os
import json
import glob


def process_json_file(input_file, output_file):
    results = {}

    # Read the input JSON file line by line
    with open(input_file, 'r') as file:
        for line in file:
            data = json.loads(line)
            # Parse the 'message' string as JSON and extract the frame number
            message_data = json.loads(data['message'].replace("'", "\""))
            frame_number = message_data['frame']
            # Subtract 1 to make frame number zero-indexed
            results[str(frame_number - 1)] = data['timestamp']

    # Write the output to the output JSON file
    with open(output_file, 'w') as file:
        json.dump(results, file, indent=4)

    print(f"Processed {input_file} -> {output_file}")


def process_directory(input_dir, output_dir):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get all JSON files in the input directory
    json_files = glob.glob(os.path.join(input_dir, '*.json'))

    for json_file in json_files:
        # Generate the output file path
        output_file_name = os.path.basename(json_file)  # Keep the same filename
        output_file = os.path.join(output_dir, output_file_name)

        # Check if the output file already exists
        if os.path.exists(output_file):
            print(f"Skipping {json_file} (already processed)")
            continue

        # Process the file if it hasn't been processed
        process_json_file(json_file, output_file)


# Define the input and output directories
input_directory = './23_06_2024/unclean_video_timestamp_data/'
output_directory = './23_06_2024/processed_video_timestamp_data/'

# Process all JSON files in the input directory
process_directory(input_directory, output_directory)

print("Batch JSON processing complete.")

