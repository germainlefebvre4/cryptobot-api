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


@router.get("/trades", response_model=List[schemas.TradesMargin])
def read_currencies(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve trades margin.
    """

    currencies = services.get_currencies_margin_trades(
        skip=skip, limit=limit,
        user_id=current_user.id)

    return currencies
