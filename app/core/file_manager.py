import boto3
import tempfile
import enum
from sqlmodel import Session
from pathlib import Path
from botocore.client import ClientError
from typing import IO
from app.core.config import settings
from app.models.files import (
        File,
        FileType,
        FileCreateHub,
        FileCreateGame,
        FileCreateUser,
        FiletypeToEnum
        )


class FileCreateType(str, enum.Enum):
    USER = "user"
    HUB = "hub"
    GAME = "game"


class FileTypeNotMatching(Exception):
    pass


class FileTypeNotAllowed(Exception):
    pass


class FileCreateTypeDoesNotExist(Exception):
    pass


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

    def create_file(self, file: IO, file_path: str,
                    create_type: FileCreateType, session: Session,
                    db_id: int, desc: str | None = None):
        ft = FiletypeToEnum(Path(file.filename).suffix)
        if create_type == FileCreateType.HUB:
            new_path = Path(f"hubs/{db_id}/") / file_path
            allowed_ft = [FileType.APWORLD, FileType.YAML]
            file_db_model = FileCreateHub(path=str(new_path), description=desc,
                                          owner_hub_id=db_id, file_type=ft)
        elif create_type == FileCreateType.USER:
            new_path = Path(f"users/{db_id}/") / file_path
            allowed_ft = [FileType.YAML]
            file_db_model = FileCreateUser(path=str(new_path),
                                           description=desc,
                                           owner_user_id=db_id,
                                           file_type=ft)
        elif create_type == FileCreateType.GAME:
            new_path = Path(f"games/{db_id}/") / file_path
            allowed_ft = [FileType.YAML, FileType.ARCHIPELAGO]
            file_db_model = FileCreateGame(path=str(new_path),
                                           description=desc,
                                           owner_game_id=db_id, file_type=ft)
        else:
            raise FileCreateTypeDoesNotExist(
                    "File Create Type {create_type} invalid"
                    )

        ft_path = FiletypeToEnum(new_path.suffix)
        if ft is not ft_path:
            raise FileTypeNotMatching(
                    f"Filetypes {ft} and {ft_path} is not the same"
                    )
        if ft not in allowed_ft:
            raise FileTypeNotAllowed(f"Filetype {ft} not allowed")

        try:
            file_manager.write(file.file, new_path)
        except Exception as e:
            raise e
        db_file = File.model_validate(file_db_model)
        session.add(db_file)
        session.commit()
        session.refresh(db_file)
        return db_file


file_manager = FileManager()
