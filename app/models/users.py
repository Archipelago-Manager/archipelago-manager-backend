from typing import List, TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship
from app.models.links import GameUserLink

if TYPE_CHECKING:
    from app.models.games import Game
    from app.models.accounts import Account
    from app.models.hubs import Hub


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
    user_id: int


class UserPublicWithGames(UserPublic):
    games: List["Game"] = []


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # user_id is the id of the user within a hub
    user_id: int | None = Field(default=None, index=True)
    games: List["Game"] = Relationship(back_populates="users",
                                       link_model=GameUserLink)
    account_id: Optional[int] = Field(default=None, foreign_key="account.id")
    account: Optional["Account"] = Relationship(back_populates="users")
    hub_id: Optional[int] = Field(default=None, foreign_key="hub.id")
    hub: Optional["Hub"] = Relationship(back_populates="users")
