from typing import List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import AnyUrl


#############################################################################
#                                 YamlFile                                  #
#############################################################################
# An archipelago game/server                                                #
#############################################################################
class GameYamlFileLink(SQLModel, table=True):
    game_id: int | None = Field(default=None, foreign_key="game.id",
                                primary_key=True)
    yaml_file_id: int | None = Field(default=None, foreign_key="yamlfile.id",
                                     primary_key=True)


class YamlFileBase(SQLModel):
    name: str
    location: str


class YamlFile(YamlFileBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    games: List["Game"] = Relationship(back_populates="yaml_files",
                                       link_model=GameYamlFileLink)
