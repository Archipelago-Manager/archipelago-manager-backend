import boto3
from app.core.config import settings


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

    def write_s3(self, file):
        pass

    def write_local(self, file):
        pass

    def write(self, file):
        if self.storage_type == "aws":
            self.write_s3(file)
        else:
            self.write_local(file)

    def read_s3(self, file):
        pass

    def read_local(self, file):
        pass

    def read(self, file):
        if self.storage_type == "aws":
            self.read_s3(file)
        else:
            self.read_local(file)
