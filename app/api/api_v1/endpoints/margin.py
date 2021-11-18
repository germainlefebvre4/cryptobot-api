import sys
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
# import json
import math
import requests

from typing import Any, List, Optional, Dict

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from sqlalchemy.orm import Session
from app.core.config import settings

from app import crud, models, schemas
from app.api import deps

from app.api import services


router = APIRouter()


@router.get("/trades/last", response_model=List[schemas.WalletCurrency])
def read_currencies(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve margin last one trade.
    """

    currencies = services.get_currencies_margin_trades_last(
        skip=skip, limit=limit,
        user_id=current_user.id)

    return currencies


@router.get("/trades/run", response_model=List[schemas.WalletCurrency])
def read_currencies(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve margin last one trade.
    """

    currencies = services.get_currencies_margin_trades_run(
        skip=skip, limit=limit,
        user_id=current_user.id)

    return currencies
