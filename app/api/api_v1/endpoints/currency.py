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


@router.get("/", response_model=List[schemas.Currency])
def read_currencies(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve currencies.
    """

    currencies = services.get_currencies(
        skip=skip, limit=limit,
        user_id=current_user.id)

    return currencies


@router.post("/", response_model=schemas.Currency)
def create_currency(
    *,
    currency_in: schemas.CurrencyCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve currencies.
    """
    currency = services.create_currency(
        user_id=current_user.id,
        currency_in=currency_in)

    return currency


@router.get("/{id}", response_model=schemas.Currency)
def read_currency(
    *,
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get currency by ID.
    """
    currency = services.get_currency_by_id(
        currency_id=id,
        user_id=current_user.id)

    if not currency:
        raise HTTPException(status_code=404, detail="Currency not found")

    return currency


@router.delete("/{id}", response_model=schemas.CurrencyDelete)
def delete_currency(
    *,
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an currency.
    """
    currency = services.delete_currency_by_id(
        currency_id=id,
        user_id=current_user.id)

    if not currency:
        raise HTTPException(status_code=404, detail="Currency not found")

    return currency
