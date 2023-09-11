import boto3
import botocore
import os
from typing import List
from tqdm import tqdm

FILE_SIZE_MB: int = 300
BUCKET_NAME: str = 'australia-fov'
PATH_PREFIX: str = 'marvel/'
REGION: str = 'ap-southeast-2'
CAMERAS: List[str] = [
    "marvel-fov-1/",
    # "marvel-fov-2/",
    # "marvel-fov-3/",
    # "marvel-fov-4/",
    # "marvel-fov-5/",
    # "marvel-fov-6/",
    # "marvel-fov-7/",
    # "marvel-fov-8/",
]

PATH_POSTFIXES: List[str] = [
    "18_08_2023/",
    # "20_08_2023/",
    # "26_08_2023/"
]


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

    def is_video_already_downloaded(self, key: str) -> bool:
        """
        Check if the video file with the given key is already downloaded locally.
        """
        local_path = os.path.join(".", key)
        return os.path.exists(local_path)

    def list_video_files(self) -> List[str]:
        video_files_to_download = []

        for camera in CAMERAS:
            for postfix in PATH_POSTFIXES:
                # Constructing the path to the desired video
                camera_path = PATH_PREFIX + camera + postfix
                response = self.s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=camera_path)

                # Filtering out only the video files and sorting them
                video_files = sorted(
                    [content['Key'] for content in response.get('Contents', []) if content['Key'].endswith('.avi')])

                # Append the second video (to get straight into gameplay!) from the list to the download list if available
                if video_files:
                    video_files_to_download.append(video_files[0])

        return video_files_to_download

    def download_partial(self, key, start_byte=0, end_byte=None) -> None:
        if self.is_video_already_downloaded(key):
            print(f"Video from key {key} is already saved locally. Skipping download.")
            return

        print(f"Trying to download from key: {key}")

        # Ensure the local path structure exists
        local_path = os.path.join(".", key)
        create_dir(os.path.dirname(local_path))

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
            with open(local_path, 'wb') as f:
                # Set up the tqdm progress bar
                with tqdm(total=file_size, unit='B', unit_scale=True, desc=local_path) as pbar:
                    # Read the content in chunks and write to destination
                    for chunk in response['Body'].iter_chunks(chunk_size=1024):
                        f.write(chunk)
                        pbar.update(len(chunk))

            print(f"Partial download of {key} completed. Saved to {local_path}.")

        except botocore.exceptions.ClientError as e:
            # Catch the specific error when a key doesn't exist
            if e.response['Error']['Code'] == "NoSuchKey":
                print(f"The key {key} does not exist.")
            else:
                # Print any other unexpected error
                print(f"An unexpected error occurred: {e}")




def main():
    downloader = S3PartialDownloader(bucket_name=BUCKET_NAME, region_name=REGION)

    video_files = downloader.list_video_files()
    for video_file in video_files:
        print(f"Preparing to download: {video_file}")
        downloader.download_partial(video_file, end_byte=FILE_SIZE_MB * 1024 * 1024)


if __name__ == "__main__":
    main()
