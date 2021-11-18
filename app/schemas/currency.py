from typing import Optional
from datetime import date, datetime

from pydantic import BaseModel

class CurrencyBase(BaseModel):
    base_currency: str
    quote_currency: str


class CurrencyCreate(CurrencyBase):
    pass


class CurrencyUpdate(BaseModel):
    pass


class CurrencyDelete(CurrencyBase):
    id: int
    user_id: int


class Currency(CurrencyBase):
    id: int
