from typing import Optional, List
from datetime import date, datetime

from pydantic import BaseModel


class MarginValue(BaseModel):
    percent: float
    value: float


class MarketPrice(BaseModel):
    price: float


class UserWallet(BaseModel):
    price: float
    volume: float


class WalletCurrency(BaseModel):
    base_currency: str
    quote_currency: str

    market: MarketPrice

    wallet: UserWallet

    margin: MarginValue


# class MarginCurrency(BaseModel):
#     currencies: List[WalletCurrency] = []
