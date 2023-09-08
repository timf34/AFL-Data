import boto3
import os
from typing import List
from tqdm import tqdm
import botocore

BUCKET_NAME: str = 'australia-fov'
PATH_PREFIX: str = 'marvel/'
REGION: str = 'ap-southeast-2'
CAMERAS: List[str] = [
    "marvel-fov-1/",
    "marvel-fov-2/",
    "marvel-fov-3/",
    "marvel-fov-4/",
    "marvel-fov-6/",
    "marvel-fov-7/",
    "marvel-fov-8/",
]
PATH_POSTFIX: str = '18_08_2023/'


def create_dir(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)


class S3PartialDownloader:
    def __init__(self, bucket_name, region_name='us-west-1'):
        """
        Initialize the downloader.

        :param bucket_name: The name of the S3 bucket.
        :param region_name: AWS region name.
        """
        self.bucket_name = bucket_name

        # Establish the S3 client
        self.s3 = boto3.client('s3', region_name=region_name)

    def download_partial(self, key, destination, start_byte=0, end_byte=None):
        print(f"Trying to download from key: {key}")

        # Define byte range for partial download
        byte_range = f"bytes={start_byte}-"
        if end_byte:
            byte_range += str(end_byte - 1)

        try:
            # Get the S3 object with the specified range
            response = self.s3.get_object(
                Bucket=self.bucket_name,
                Key=key,
                Range=byte_range
            )

            # Extract the content length of the partial file for tqdm
            file_size = int(response['ContentLength'])

            # Open the destination file for binary write
            with open(destination, 'wb') as f:
                # Set up the tqdm progress bar
                with tqdm(total=file_size, unit='B', unit_scale=True, desc=destination) as pbar:
                    # Read the content in chunks and write to destination
                    for chunk in response['Body'].iter_chunks(chunk_size=1024):
                        f.write(chunk)
                        pbar.update(len(chunk))

            print(f"Partial download of {key} completed. Saved to {destination}.")

        except botocore.exceptions.ClientError as e:
            # Catch the specific error when a key doesn't exist
            if e.response['Error']['Code'] == "NoSuchKey":
                print(f"The key {key} does not exist.")
            else:
                # Print any other unexpected error
                print(f"An unexpected error occurred: {e}")


def main():
    downloader = S3PartialDownloader(bucket_name=BUCKET_NAME, region_name=REGION)

    # Constructing the path to the desired video
    camera_path = PATH_PREFIX + CAMERAS[0] + PATH_POSTFIX + "time_10_54_04_date_19_08_2023_.avi"

    # Start the download, aiming for the first 50MB
    downloader.download_partial(camera_path, 'destination_path.mp4', 0, 50 * 1024 * 1024)


if __name__ == "__main__":
    main()
