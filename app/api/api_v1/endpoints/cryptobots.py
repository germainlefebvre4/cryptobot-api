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


@router.get("/", response_model=List[schemas.Cryptobot])
def read_cryptobots(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve cryptobots.
    """
    if crud.user.is_superuser(current_user):
        cryptobots = crud.cryptobot.get_multi(db, skip=skip, limit=limit)
    else:
        cryptobots = crud.cryptobot.get_multi_by_user(
            db=db, user_id=current_user.id, skip=skip, limit=limit
        )

    return cryptobots


@router.post("/", response_model=schemas.Cryptobot)
def create_cryptobot(
    *,
    db: Session = Depends(deps.get_db),
    binance_account_id: int,
    telegram_id: int,
    cryptobot_in: schemas.CryptobotCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new cryptobot.
    """
    if crud.user.get(db, id=current_user.id):
        pass
    else:
        raise HTTPException(status_code=400, detail="User not found")

    binance_account = crud.binance_account.get(db, id=binance_account_id)
    if binance_account:
        pass
    else:
        raise HTTPException(status_code=400, detail="Binance Account not found")

    telegram = crud.telegram.get(db, id=telegram_id)
    if telegram:
        pass
    else:
        raise HTTPException(status_code=400, detail="Telegram not found")

    cryptobot_in.binance_config_base_currency = cryptobot_in.binance_config_base_currency.upper()
    cryptobot_in.binance_config_quote_currency = cryptobot_in.binance_config_quote_currency.upper()
    
    post_data = {}
    post_data['user_id'] = current_user.id
    post_data['binance_api_key'] = binance_account.binance_api_key
    post_data['binance_api_secret'] = binance_account.binance_api_secret
    post_data['telegram_client_id'] = telegram.client_id
    post_data['telegram_token'] = telegram.token
    for key,val in cryptobot_in.__dict__.items():
        if isinstance(val, bool) and val:
            post_data[key] = 1
        elif isinstance(val, bool) and not val:
            post_data[key] = 0
        else:
            post_data[key] = val

    services.create_operator_bot(post_data)

    cryptobot = crud.cryptobot.create_with_owner(
        db=db, obj_in=cryptobot_in,
        user_id=current_user.id,
        binance_account_id=binance_account_id,
        telegram_id=telegram_id,
    )

    return cryptobot


@router.put("/{id}", response_model=schemas.Cryptobot)
def update_cryptobot(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    cryptobot_in: schemas.CryptobotUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an cryptobot.
    """
    cryptobot = crud.cryptobot.get(db=db, id=id)

    if not cryptobot:
        raise HTTPException(status_code=404, detail="Cryptobot not found")
    if (not crud.user.is_superuser(current_user) and
            (cryptobot.user_id != current_user.id)):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    post_data = {}
    post_data['user_id'] = current_user.id
    post_data['binance_api_key'] = cryptobot.binance_account.binance_api_key
    post_data['binance_api_secret'] = cryptobot.binance_account.binance_api_secret
    post_data['telegram_client_id'] = cryptobot.telegram.client_id
    post_data['telegram_token'] = cryptobot.telegram.token
    for key,val in cryptobot_in.__dict__.items():
        if isinstance(val, bool) and val:
            post_data[key] = 1
        elif isinstance(val, bool) and not val:
            post_data[key] = 0
        else:
            post_data[key] = val

    bot_name = f"{current_user.id}-{cryptobot.binance_config_base_currency}{cryptobot.binance_config_quote_currency}".lower()
    res = services.update_operator_bot(bot_name, post_data)

    cryptobot = crud.cryptobot.update(db=db, db_obj=cryptobot, obj_in=cryptobot_in)

    return cryptobot


@router.get("/{id}", response_model=schemas.Cryptobot)
def read_cryptobot(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get cryptobot by ID.
    """
    cryptobot = crud.cryptobot.get(db=db, id=id)

    if not cryptobot:
        raise HTTPException(status_code=404, detail="Cryptobot not found")
    if (not crud.user.is_superuser(current_user) and
            (cryptobot.user_id != current_user.id)):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    return cryptobot


@router.get("/{id}/status", response_model=schemas.CryptobotStatus)
def read_cryptobot_status(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get cryptobot by ID.
    """
    cryptobot = crud.cryptobot.get(db=db, id=id)

    if not cryptobot:
        raise HTTPException(status_code=404, detail="Cryptobot not found")
    if (not crud.user.is_superuser(current_user) and
            (cryptobot.user_id != current_user.id)):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    bot_name = f"{current_user.id}-{cryptobot.binance_config_base_currency}{cryptobot.binance_config_quote_currency}".lower()
    bot_status = services.get_bot_status(bot_name)

    return bot_status


@router.get("/{id}/logs", response_model=schemas.CryptobotLogs)
def read_cryptobot_logs(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get cryptobot by ID.
    """
    cryptobot = crud.cryptobot.get(db=db, id=id)

    if not cryptobot:
        raise HTTPException(status_code=404, detail="Cryptobot not found")
    if (not crud.user.is_superuser(current_user) and
            (cryptobot.user_id != current_user.id)):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    bot_name = f"{current_user.id}-{cryptobot.binance_config_base_currency}{cryptobot.binance_config_quote_currency}".lower()
    bot_logs = services.get_bot_logs(bot_name)

    return bot_logs


@router.get("/{id}/version", response_model=schemas.CryptobotVersion)
def read_cryptobot_version(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get cryptobot by ID.
    """
    cryptobot = crud.cryptobot.get(db=db, id=id)

    if not cryptobot:
        raise HTTPException(status_code=404, detail="Cryptobot not found")
    if (not crud.user.is_superuser(current_user) and
            (cryptobot.user_id != current_user.id)):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    bot_name = f"{current_user.id}-{cryptobot.binance_config_base_currency}{cryptobot.binance_config_quote_currency}".lower()
    bot_version = services.get_bot_version(bot_name)

    return bot_version


@router.get("/{id}/margin/trades/current/last", response_model=schemas.CryptobotMarginLastTrade)
def get_bot_margin_trades_current_last(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get cryptobot by ID.
    """
    cryptobot = crud.cryptobot.get(db=db, id=id)

    if not cryptobot:
        raise HTTPException(status_code=404, detail="Cryptobot not found")
    if (not crud.user.is_superuser(current_user) and
            (cryptobot.user_id != current_user.id)):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    bot_margin_trades_current_last = services.get_bot_margin_trades_current_last(
        base_currency=cryptobot.binance_config_base_currency,
        quote_currency=cryptobot.binance_config_quote_currency,
        user_id=current_user.id)

    return bot_margin_trades_current_last


@router.get("/{id}/margin/trades/current/run", response_model=schemas.CryptobotMarginOverall)
def get_bot_margin_trades_current_run(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get cryptobot by ID.
    """
    cryptobot = crud.cryptobot.get(db=db, id=id)

    if not cryptobot:
        raise HTTPException(status_code=404, detail="Cryptobot not found")
    if (not crud.user.is_superuser(current_user) and
            (cryptobot.user_id != current_user.id)):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    bot_margin_trades_current_run = services.get_bot_margin_trades_current_run(
        base_currency=cryptobot.binance_config_base_currency,
        quote_currency=cryptobot.binance_config_quote_currency,
        user_id=current_user.id)

    return bot_margin_trades_current_run


@router.get("/{id}/margin/trades/history/sell", response_model=schemas.CryptobotMarginOverall)
def get_bot_margin_trades_history_sells(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get cryptobot by ID.
    """
    cryptobot = crud.cryptobot.get(db=db, id=id)

    if not cryptobot:
        raise HTTPException(status_code=404, detail="Cryptobot not found")
    if (not crud.user.is_superuser(current_user) and
            (cryptobot.user_id != current_user.id)):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    bot_margin_trades_history_sells = services.get_bot_margin_trades_history_sells(
        base_currency=cryptobot.binance_config_base_currency,
        quote_currency=cryptobot.binance_config_quote_currency,
        user_id=current_user.id)

    return bot_margin_trades_history_sells


@router.get("/{id}/margin/trades/history/all", response_model=schemas.CryptobotMarginLastTrade)
def get_bot_margin_trades_history_all(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get cryptobot by ID.
    """
    cryptobot = crud.cryptobot.get(db=db, id=id)

    if not cryptobot:
        raise HTTPException(status_code=404, detail="Cryptobot not found")
    if (not crud.user.is_superuser(current_user) and
            (cryptobot.user_id != current_user.id)):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    bot_margin_trades_history_all = services.get_bot_margin_trades_history_all(
        base_currency=cryptobot.binance_config_base_currency,
        quote_currency=cryptobot.binance_config_quote_currency,
        user_id=current_user.id)

    return bot_margin_trades_history_all


@router.delete("/{id}", response_model=schemas.CryptobotDelete)
def delete_cryptobot(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an cryptobot.
    """
    cryptobot = crud.cryptobot.get(db=db, id=id)

    if not cryptobot:
        raise HTTPException(status_code=404, detail="Cryptobot not found")
    if (not crud.user.is_superuser(current_user) and
            (cryptobot.user_id != current_user.id)):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    bot_name = f"{current_user.id}-{cryptobot.binance_config_base_currency}{cryptobot.binance_config_quote_currency}".lower()
    services.delete_operator_bot(bot_name)
    
    cryptobot = crud.cryptobot.remove(db=db, id=id)

    return cryptobot
