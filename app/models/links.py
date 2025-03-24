from sqlmodel import SQLModel, Field


class GameYamlFileLink(SQLModel, table=True):
    game_id: int | None = Field(default=None, foreign_key="game.id",
                                primary_key=True)
    yaml_file_id: int | None = Field(default=None, foreign_key="yamlfile.id",
                                     primary_key=True)


class GameUserLink(SQLModel, table=True):
    game_id: int | None = Field(default=None, foreign_key="game.id",
                                primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id",
                                primary_key=True)


class HubUserLink(SQLModel, table=True):
    hub_id: int | None = Field(default=None, foreign_key="hub.id",
                               primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id",
                                primary_key=True)


class HubGameLink(SQLModel, table=True):
    hub_id: int | None = Field(default=None, foreign_key="hub.id",
                               primary_key=True)
    game_id: int | None = Field(default=None, foreign_key="game.id",
                                primary_key=True)
