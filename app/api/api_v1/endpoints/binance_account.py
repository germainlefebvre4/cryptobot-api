from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import json
import math
import requests

from typing import Any, List, Optional, Dict

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from sqlalchemy.orm import Session
from app.core.config import settings

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.BinanceAccount])
def read_binance_accounts(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve binance_accounts.
    """
    if crud.user.is_superuser(current_user):
        binance_accounts = crud.binance_account.get_multi(db, skip=skip, limit=limit)
    else:
        binance_accounts = crud.binance_account.get_multi_by_user(
            db=db, user_id=current_user.id, skip=skip, limit=limit
        )

    return binance_accounts


@router.post("/", response_model=schemas.BinanceAccount)
def create_binance_account(
    *,
    db: Session = Depends(deps.get_db),
    binance_account_in: schemas.BinanceAccountCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new binance_account.
    """
    if crud.user.get(db, id=current_user.id):
        pass
    else:
        raise HTTPException(status_code=400, detail="User not found")
    
    binance_account = crud.binance_account.create_with_owner(
        db=db, obj_in=binance_account_in, user_id=current_user.id)

    return binance_account


@router.put("/{id}", response_model=schemas.BinanceAccount)
def update_binance_account(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    binance_account_in: schemas.BinanceAccountUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an binance_account.
    """
    binance_account = crud.binance_account.get(db=db, id=id)

    if not binance_account:
        raise HTTPException(status_code=404, detail="BinanceAccount not found")
    if (not crud.user.is_superuser(current_user) and
            (binance_account.user_id != current_user.id)):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    binance_account = crud.binance_account.update(db=db, db_obj=binance_account, obj_in=binance_account_in)

    return binance_account


@router.get("/{id}", response_model=schemas.BinanceAccount)
def read_binance_account(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get binance_account by ID.
    """
    binance_account = crud.binance_account.get(db=db, id=id)

    if not binance_account:
        raise HTTPException(status_code=404, detail="BinanceAccount not found")
    if (not crud.user.is_superuser(current_user) and
            (binance_account.user_id != current_user.id)):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    return binance_account


@router.delete("/{id}", response_model=schemas.BinanceAccountDelete)
def delete_binance_account(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an binance_account.
    """
    binance_account = crud.binance_account.get(db=db, id=id)

    if not binance_account:
        raise HTTPException(status_code=404, detail="BinanceAccount not found")
    if (not crud.user.is_superuser(current_user) and
            (binance_account.user_id != current_user.id)):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    binance_account = crud.binance_account.remove(db=db, id=id)

    return binance_account
