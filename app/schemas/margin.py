from typing import Optional, List
from datetime import date, datetime

from pydantic import BaseModel


class MarginValue(BaseModel):
    percent: float
    value: float


class MarginTradeOperations(BaseModel):
    count: int


class MarginTrade(BaseModel):
    operations: MarginTradeOperations
    price: float
    volume: float
    value: float
    margin: MarginValue


class MarketPrice(BaseModel):
    price: float


class UserWallet(BaseModel):
    price: float
    volume: float


class TradesMargin(BaseModel):
    base_currency: Optional[str]
    quote_currency: Optional[str]

    market: Optional[MarketPrice]
    wallet: Optional[UserWallet]

    last_trade: Optional[MarginTrade]
    last_run: Optional[MarginTrade]
