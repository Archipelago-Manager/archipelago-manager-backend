from typing import List, TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship
from app.models.links import HubGameLink

if TYPE_CHECKING:
    from app.models.users import User, UserPublic
    from app.models.games import Game, GamePublic
    from app.models.accounts import Account


#############################################################################
#                                   HUB                                     #
#############################################################################
# A hub where several games and users are collected                         #
#############################################################################
class HubBase(SQLModel):
    name: str = Field(index=True, unique=True, min_length=1)
    description: str | None = Field(default=None)


class HubCreate(HubBase):
    pass


class HubPublic(HubBase):
    id: int


class HubPrivate(HubBase):
    id: int
    users: List["UserPublic"] = []
    games: List["GamePublic"] = []


class Hub(HubBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    owner_id: Optional[int] = Field(default=None, foreign_key="account.id")
    owner: Optional["Account"] = Relationship(back_populates="owned_hubs")
    users: List["User"] = Relationship(back_populates="hub")
    games: List["Game"] = Relationship(back_populates="hubs",
                                       link_model=HubGameLink)
