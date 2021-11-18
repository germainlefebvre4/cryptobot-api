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
    base_currency: Optional[str]
    quote_currency: Optional[str]

    market: Optional[MarketPrice]

    wallet: Optional[UserWallet]

    margin: Optional[MarginValue]
