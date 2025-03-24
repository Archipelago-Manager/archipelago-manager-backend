from typing import List, TYPE_CHECKING
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.hubs import Hub
    from app.models.users import User


#############################################################################
#                                 ACCOUNT                                   #
#############################################################################
# An account on the website, can be in several hubs, own hubs and be        #
# connected to several users (in different hubs)                            #
#############################################################################
class AccountBase(SQLModel):
    account_name: str = Field(unique=True, index=True,
                              max_length=255)
    email: EmailStr = Field(unique=True, index=True,
                            max_length=255)
    is_superuser: bool = False


class AccountCreate(AccountBase):
    password: str = Field(min_length=8, max_length=128)


class AccountRegister(SQLModel):
    account_name: str = Field(unique=True, index=True,
                              max_length=255)
    email: EmailStr = Field(unique=True, index=True,
                            max_length=255)
    password: str = Field(min_length=8, max_length=128)


class AccountPublic(AccountBase):
    id: int


class Account(AccountBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hased_password: str
    owned_hubs: List["Hub"] = Relationship(back_populates="owner")
    users: List["User"] = Relationship(back_populates="account")
