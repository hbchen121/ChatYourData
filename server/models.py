from typing import Optional
from pydantic import BaseModel
from sqlalchemy import (Column, PrimaryKeyConstraint, String)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# User Accounts

class UserModel(BaseModel):
    username: str

    class Config:
        orm_mode = True

class UserWithHashModel(UserModel):
    password: str

class UserOrm(Base):
    __tablename__ = 'users'
    username = Column(String, unique=True)
    password = Column(String)
    PrimaryKeyConstraint(username)

    def __repr__(self):
        return "<UserOrm(username='{0}', password='{2}')>".format(self.username, self.password)

# Tokens

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(Token):
    username: Optional[str] = None
