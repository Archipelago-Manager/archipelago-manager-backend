from typing import List, TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship
from app.models.links import GameUserLink, GameYamlFileLink

if TYPE_CHECKING:
    from app.models.configs import YamlFile
    from app.models.users import User, UserPublic
    from app.models.hubs import Hub


#############################################################################
#                                   GAME                                    #
#############################################################################
# An archipelago game/server                                                #
#############################################################################
class GameBase(SQLModel):
    name: str = Field(index=True)
    game_id: int


class GameCreate(SQLModel):
    name: str = Field(index=True)


class GameCreateInternal(GameBase):
    hub_id: int


class GamePublic(GameBase):
    pass


class GamePublicWithUsers(GamePublic):
    users: List["UserPublic"] = []


class Game(GameBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # game_id is the id of the game within a hub
    game_id: int | None = Field(index=True)
    node_address: str | None = None
    node_port: int | None = None
    yaml_files: List["YamlFile"] = Relationship(back_populates="games",
                                                link_model=GameYamlFileLink)
    users: List["User"] = Relationship(back_populates="games",
                                       link_model=GameUserLink)
    hub_id: int = Field(foreign_key="hub.id")
    hub: Optional["Hub"] = Relationship(back_populates="games")
