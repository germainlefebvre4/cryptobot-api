from typing import Optional

from pydantic import BaseModel


class TelegramBase(BaseModel):
    client_id: str
    token: str


class TelegramCreate(TelegramBase):
    client_id: str
    token: str


class Telegram(TelegramBase):
    pass
