import boto3
from typing import List

BUCKET_NAME: str = 'australia-fov'
PATH_PREFIX: str = 'marvel/'
REGION: str = 'ap-southeast-2'
CAMERAS: List[str] = [
    "marvel-fov-2/",
    "marvel-fov-3/",
    "marvel-fov-4/",
    "marvel-fov-6/",
    "marvel-fov-7/",
    "marvel-fov-8/",
]
PATH_POSTFIX: str = '18_08_2023/'

class S3PartialDownloader:
    def __init__(self, bucket_name, region_name='us-west-1'):
        """
        Initialize the downloader.

        :param bucket_name: The name of the S3 bucket.
        :param region_name: AWS region name.
        """
        self.bucket_name = bucket_name

        # Establishing the S3 client
        self.s3 = boto3.client('s3', region_name=region_name)

    def download_partial(self, key, destination, start_byte=0, end_byte=None):
        """
        Download a partial range from a file in S3.

        :param key: The key of the S3 object.
        :param destination: The path to save the partial download.
        :param start_byte: The starting byte (inclusive).
        :param end_byte: The ending byte (exclusive).
        """
        byte_range = f"bytes={start_byte}-"
        if end_byte:
            byte_range += str(end_byte - 1)  # Since the end_byte is exclusive, we reduce by 1

        response = self.s3.get_object(
            Bucket=self.bucket_name,
            Key=key,
            Range=byte_range
        )

        with open(destination, 'wb') as f:
            f.write(response['Body'].read())


def main():
    downloader = S3PartialDownloader(bucket_name=BUCKET_NAME)

    # Example usage for one of the cameras
    camera_path = PATH_PREFIX + CAMERAS[
        5] + PATH_POSTFIX + "time_10_54_04_date_19_08_2023_.avi"  # replace 'specific_video_filename.mp4' with the actual filename
    downloader.download_partial(camera_path, 'destination_path.mp4', 0,
                                50 * 1024 * 1024)  # This will download the first 100MB


if __name__ == "__main__":
    main()
