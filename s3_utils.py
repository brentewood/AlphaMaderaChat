"""Utility module for AWS S3 operations including file upload, download, and URL handling."""

import boto3
from botocore.exceptions import NoCredentialsError
import requests

class S3Utils:
    """Utility class for AWS S3 operations including file upload, download, and URL operations."""

    def __init__(self, access_key, secret_key, region_name, bucket_name):
        """Initialize S3 client with credentials and bucket information.

        Args:
            access_key (str): AWS access key ID
            secret_key (str): AWS secret access key
            region_name (str): AWS region name
            bucket_name (str): S3 bucket name
        """
        self._s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region_name)
        self._bucket_name = bucket_name

    def upload_file(self, local_file_path, s3_file_path):
        """Upload a local file to S3.

        Args:
            local_file_path (str): Path to local file
            s3_file_path (str): Destination path in S3
        """
        with open(local_file_path, 'rb') as file:
            self._s3.upload_fileobj(file, self._bucket_name, s3_file_path)
        print(f"Uploaded file {local_file_path} to S3 bucket {self._bucket_name} as {s3_file_path}.")

    def download_file_from_s3(self, s3_file_path, local_file_path):
        """Download a file from S3 to local storage.

        Args:
            s3_file_path (str): Path of file in S3
            local_file_path (str): Destination path for local file
        """
        with open(local_file_path, 'wb') as file:
            self._s3.download_fileobj(self._bucket_name, s3_file_path, file)
        print(f"Downloaded file {s3_file_path} from S3 bucket {self._bucket_name} as {local_file_path}.")

    def down_file_from_url(self, remote_url, local_file_path):
        """Download a file from a URL to local storage.

        Args:
            remote_url (str): URL of the file to download
            local_file_path (str): Destination path for local file

        Returns:
            bool: True if download successful, False otherwise
        """
        response = requests.get(remote_url, stream=True, timeout=30)
        if response.status_code == 200:
            with open(local_file_path, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded file {remote_url} to {local_file_path}.")
            return True
        else:
            print(f"Failed to fetch the file from {remote_url}. Status code: {response.status_code}")
            return False

    def upload_from_url_to_s3(self, remote_url, s3_key) -> bool:
        """Upload a file from a URL directly to S3.

        Args:
            remote_url (str): URL of the file to upload
            s3_key (str): Destination path in S3

        Returns:
            bool: True if upload successful, False otherwise
        """
        response = requests.get(remote_url, stream=True, timeout=60)

        if response.status_code == 200:
            try:
                self._s3.upload_fileobj(response.raw, self._bucket_name, s3_key)
                print(f"File uploaded to s3://{self._bucket_name}/{s3_key}")
                return True
            except NoCredentialsError:
                print("Credentials not available")
        else:
            print(f"Failed to fetch the file from {remote_url}. Status code: {response.status_code}")

        return False

    def head_file(self, s3_file_path):
        """Check if a file exists in S3."""
        try:
            self._s3.head_object(Bucket=self._bucket_name, Key=s3_file_path)
            return True
        except (NoCredentialsError, self._s3.exceptions.ClientError):
            return False

    def object_size(self, s3_file_path):
        """Get the size of an S3 object in bytes."""
        try:
            response = self._s3.head_object(Bucket=self._bucket_name, Key=s3_file_path)
            return response['ContentLength']
        except (NoCredentialsError, self._s3.exceptions.ClientError):
            return 0