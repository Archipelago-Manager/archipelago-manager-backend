import boto3
import tempfile
from pathlib import Path
from botocore.client import ClientError
from typing import IO
from app.core.config import settings


class FileManager():
    def __init__(self):
        if settings.STORAGE_TYPE == "aws":
            self.storage_type = "aws"
            if settings.AWS_ENDPOINT_URL:
                self.s3 = boto3.resource(
                        's3',
                        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                        endpoint_url=settings.AWS_ENDPOINT_URL
                        )
            else:
                self.s3 = boto3.resource(
                        's3',
                        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                        region_name="ap-south-1"
                        )
            try:
                self.s3.meta.client.head_bucket(
                        Bucket=settings.AWS_BUCKET_NAME
                        )
            except ClientError:
                # Bucket does not exist
                self.bucket = self.s3.create_bucket(
                        Bucket=settings.AWS_BUCKET_NAME
                        )
        else:
            self.storage_type = "local"

    def _write_s3(self, file: IO, save_path: str) -> None:
        self.s3.Bucket(settings.AWS_BUCKET_NAME).upload_fileobj(
                Fileobj=file, Key=save_path
                )

    def _write_local(self, file: IO, save_path: str) -> None:
        filepath = Path(settings.LOCAL_STORAGE_ROOT_FOLDER) / save_path
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'wb') as f:
            f.write(file.read())

    def write(self, file: IO, save_path: str) -> None:
        if self.storage_type == "aws":
            self._write_s3(file, save_path)
        else:
            self._write_local(file, save_path)

    def _read_s3(self, file_path: str) -> IO:
        tf = tempfile.NamedTemporaryFile()
        self.s3.Bucket(settings.AWS_BUCKET_NAME).download_fileobj(file_path,
                                                                  tf)
        tf.seek(0)
        return tf

    def _read_local(self, file_path: str) -> IO:
        tf = tempfile.NamedTemporaryFile()
        filepath = Path(settings.LOCAL_STORAGE_ROOT_FOLDER) / file_path
        with open(filepath, "rb") as f:
            read_bytes = f.read()
            tf.write(read_bytes)
            tf.seek(0)
        return tf

    def read(self, file_path: str) -> IO:
        if self.storage_type == "aws":
            return self._read_s3(file_path)
        else:
            return self._read_local(file_path)


file_manager = FileManager()
