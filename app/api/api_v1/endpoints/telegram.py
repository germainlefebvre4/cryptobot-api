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


@router.get("/", response_model=List[schemas.Telegram])
def read_telegrams(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve telegrams.
    """
    if crud.user.is_superuser(current_user):
        telegrams = crud.telegram.get_multi(db, skip=skip, limit=limit)
    else:
        telegrams = crud.telegram.get_multi_by_user(
            db=db, user_id=current_user.id, skip=skip, limit=limit
        )

    return telegrams


@router.post("/", response_model=schemas.Telegram)
def create_telegram(
    *,
    db: Session = Depends(deps.get_db),
    telegram_in: schemas.TelegramCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new telegram.
    """
    if crud.user.get(db, id=current_user.id):
        pass
    else:
        raise HTTPException(status_code=400, detail="User not found")
    
    telegram = crud.telegram.create_with_owner(
        db=db, obj_in=telegram_in, user_id=current_user.id)

    return telegram


@router.put("/{id}", response_model=schemas.Telegram)
def update_telegram(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    telegram_in: schemas.TelegramUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an telegram.
    """
    telegram = crud.telegram.get(db=db, id=id)

    if not telegram:
        raise HTTPException(status_code=404, detail="Telegram not found")
    if (not crud.user.is_superuser(current_user) and
            (telegram.user_id != current_user.id)):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    telegram = crud.telegram.update(db=db, db_obj=telegram, obj_in=telegram_in)

    return telegram


@router.get("/{id}", response_model=schemas.Telegram)
def read_telegram(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get telegram by ID.
    """
    telegram = crud.telegram.get(db=db, id=id)

    if not telegram:
        raise HTTPException(status_code=404, detail="Telegram not found")
    if (not crud.user.is_superuser(current_user) and
            (telegram.user_id != current_user.id)):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    return telegram


@router.delete("/{id}", response_model=schemas.TelegramDelete)
def delete_telegram(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an telegram.
    """
    telegram = crud.telegram.get(db=db, id=id)

    if not telegram:
        raise HTTPException(status_code=404, detail="Telegram not found")
    if (not crud.user.is_superuser(current_user) and
            (telegram.user_id != current_user.id)):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    telegram = crud.telegram.remove(db=db, id=id)

    return telegram
