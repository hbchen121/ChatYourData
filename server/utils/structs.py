# encoding:utf-8
from pydantic import BaseModel


class UserDetails(BaseModel):
    username: str
    access_token: str
    token_type: str


class AddLink(BaseModel):
    link: str
    user: UserDetails  # client / src / views / AddLink.vue: 24
    # user: dict  # client / src / views / AddLink.vue: 24


class Apikey(BaseModel):
    apikey: str
    user: UserDetails  # client/src/views/Apikey.vue:23
    # user: dict  # client/src/views/Apikey.vue:23


class User(BaseModel):
    user: UserDetails
