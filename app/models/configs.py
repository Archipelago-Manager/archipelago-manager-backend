from typing import List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from app.models.links import GameYamlFileLink

if TYPE_CHECKING:
    from app.models.games import Game


#############################################################################
#                                 YamlFile                                  #
#############################################################################
# Yaml files used for configurations                                        #
#############################################################################
class YamlFileBase(SQLModel):
    name: str
    location: str


class YamlFile(YamlFileBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    games: List["Game"] = Relationship(back_populates="yaml_files",
                                       link_model=GameYamlFileLink)
