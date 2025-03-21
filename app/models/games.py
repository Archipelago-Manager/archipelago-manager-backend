from typing import List
from sqlmodel import SQLModel, Field, Relationship
from app.models.configs import GameYamlFileLink
from app.models.users import GameUserLink


#############################################################################
#                                   GAME                                    #
#############################################################################
# An archipelago game/server                                                #
#############################################################################
class GameBase(SQLModel):
    pass


class GameCreate(GameBase):
    pass


class Game(GameBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    node_address: str | None = None
    node_port: int | None = None
    yaml_files: List["YamlFile"] = Relationship(back_populates="games",
                                                link_model=GameYamlFileLink)
    users: List["User"] = Relationship(back_populates="games",
                                       link_model=GameUserLink)
