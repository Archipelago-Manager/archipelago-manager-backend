import enum
from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.users import User
    from app.models.games import Game
    from app.models.hubs import Hub


class FileType(str, enum.Enum):
    YAML = "yaml"
    ARCHIPELAGO = "archipelago"
    APWORLD = "apworld"
    OTHER = "OTHER"


def FiletypeToEnum(suffix: str) -> FileType:
    if suffix == ".yml" or suffix == ".yaml":
        return FileType.YAML
    elif suffix == ".archipelago":
        return FileType.ARCHIPELAGO
    elif suffix == ".apworld":
        return FileType.APWORLD
    else:
        return FileType.OTHER


#############################################################################
#                                   HUB                                     #
#############################################################################
# A hub where several games and users are collected                         #
#############################################################################
class FileBase(SQLModel):
    path: str = Field(index=True, unique=True, min_length=1)
    description: str | None = Field(default=None)
    file_type: Optional[FileType]


class FileCreateHub(FileBase):
    owner_hub_id: int
    file_type: FileType


class FileCreateUser(FileBase):
    owner_user_id: int
    file_type: FileType


class FileCreateGame(FileBase):
    owner_game_id: int
    file_type: FileType


class FilePublic(FileBase):
    id: int
    file_type: FileType


class FilePrivate(FileBase):
    id: int
    file_type: FileType


class File(FileBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    owner_user_id: Optional[int] = Field(default=None,
                                         foreign_key="user.id")
    owner_user: Optional["User"] = Relationship(back_populates="files")
    owner_game_id: Optional[int] = Field(default=None,
                                         foreign_key="game.id")
    owner_game: Optional["Game"] = Relationship(back_populates="files")
    owner_hub_id: Optional[int] = Field(default=None,
                                        foreign_key="hub.id")
    owner_hub: Optional["Hub"] = Relationship(back_populates="files")
