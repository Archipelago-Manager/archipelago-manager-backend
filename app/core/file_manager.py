import boto3
import tempfile
from app.core.config import settings
from typing import IO


class FileManager():
    def __init__(self):
        if settings.STORAGE_TYPE == "aws":
            self.storage_type = "aws"
            self.s3 = boto3.resource(
                    's3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name="ap-south-1"
                    )
        else:
            self.storage_type = "local"

    def write_s3(self, file: IO) -> None:
        self.s3.Bucket(settings.AWS_BUCKET_NAME).upload_fileobj(
                Fileobj=file, Key=file.name
                )

    def write_local(self, file: IO, root_folder_name: str) -> None:
        pass

    def write(self, file: IO) -> None:
        if self.storage_type == "aws":
            self.write_s3(file)
        else:
            self.write_local(file)

    def read_s3(self, file_name: str) -> IO:
        tf = tempfile.TemporaryFile()
        self.s3.Bucket(settings.AWS_BUCKET_NAME).download_fileobj(file_name,
                                                                  tf)
        return tf

    def read_local(self, file_name: str) -> IO:
        tf = tempfile.TemporaryFile()
        return tf

    def read(self, file_name: str) -> IO:
        if self.storage_type == "aws":
            return self.read_s3(file_name)
        else:
            return self.read_local(file_name)
