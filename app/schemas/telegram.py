from typing import Optional
from datetime import date, datetime

from pydantic import BaseModel
from app.schemas.user import User


class TelegramBase(BaseModel):
    client_id: str
    token: str


class TelegramCreate(TelegramBase):
    client_id: str
    token: str


class TelegramUpdate(BaseModel):
    client_id: str
    token: str


class TelegramDelete(TelegramBase):
    id: int

    class Config:
        orm_mode = True


class TelegramInDBBase(TelegramBase):
    id: int
    
    created_on: Optional[datetime]
    updated_on: Optional[datetime]

    class Config:
        orm_mode = True


class Telegram(TelegramInDBBase):
    pass


class TelegramInDB(TelegramInDBBase):
    pass
