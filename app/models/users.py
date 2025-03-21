from typing import List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from app.models.links import GameUserLink

if TYPE_CHECKING:
    from app.models.games import Game


#############################################################################
#                                   USER                                    #
#############################################################################
# A user on a server, not neccessarily an account                           #
#############################################################################
class UserBase(SQLModel):
    name: str = Field(max_length=255)


class UserCreate(UserBase):
    pass


class UserPublic(UserBase):
    id: int


class UserPublicWithGames(UserPublic):
    games: List["Game"]


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    games: List["Game"] = Relationship(back_populates="users",
                                       link_model=GameUserLink)
