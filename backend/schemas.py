from typing import Union
from typing_extensions import Annotated
from pydantic import BaseModel, ConfigDict, PlainSerializer

from settings import IMAGE_FOLDER


ImagePath = Annotated[
    str, PlainSerializer(lambda image_name: f'{IMAGE_FOLDER}/{image_name}', 
                         return_type=str)
]


class ItemBase(BaseModel):
    title: str
    description: str | None = None
    price: int
    image_name: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    image_name: ImagePath


class User(BaseModel):
    username: str
    disabled: Union[bool, None] = None


class UserInDB(User):
    model_config = ConfigDict(from_attributes=True)

    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str
