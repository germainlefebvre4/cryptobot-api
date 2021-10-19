from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import json
import math
import requests

from typing import Any, List, Optional, Dict

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from fastapi.security.api_key import APIKey

from sqlalchemy.orm import Session
from app.core.config import settings

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.BinanceAccount])
def read_binance_account_by_user_private(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    api_key: APIKey = Depends(deps.get_api_key),
) -> Any:
    """
    Get binance_account.
    """
    binance_accounts = crud.binance_account.get_multi_by_user(db=db, user_id=user_id)

    return binance_accounts
