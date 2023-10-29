from dataclasses import field
from typing import List, Optional

from pydantic import BaseModel


class RegisterUserRequest(BaseModel):
    name: str
    surname: str
    age: int


class UserModel(BaseModel):
    id: int
    name: str
    surname: str
    age: int

    class Config:
        from_attributes = True


class CreateCityRequest(BaseModel):
    name: str


class City(BaseModel):
    id: int
    name: str
    weather: float


class RegisterUserRequest(BaseModel):
    name: str
    surname: str
    age: int


class UserModel(BaseModel):
    id: int
    name: str
    surname: str
    age: int

    class Config:
        from_attributes = True


class Picnic(BaseModel):
    id: int
    city_id: str
    time: str
    users: List[Optional[UserModel]] = field(default_factory=list)

    class Config:
        from_attributes = True


class PicnicAddResponse(BaseModel):
    id: int
    city: str
    time: str


class PicnicResponse(BaseModel):
    id: int
    city: str
    time: str
    users: List[Optional[UserModel]] = field(default_factory=list)


class PicnicRegistrationResponse(BaseModel):
    id: int
    user: UserModel
    picnic: PicnicAddResponse

