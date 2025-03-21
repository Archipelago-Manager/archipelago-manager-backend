from typing import List
from sqlmodel import SQLModel, Field, Relationship


#############################################################################
#                                   USER                                    #
#############################################################################
# A user on a server, not neccessarily an account                           #
#############################################################################
class GameUserLink(SQLModel, table=True):
    game_id: int | None = Field(default=None, foreign_key="game.id",
                                primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id",
                                primary_key=True)


class UserBase(SQLModel):
    name: str = Field(max_length=255)


class UserCreate(UserBase):
    pass


class UserPublic(UserBase):
    pass


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    games: List["Game"] = Relationship(back_populates="users",
                                       link_model=GameUserLink)
