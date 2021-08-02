from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    cryptobots,login, users, utils, binance_account, telegram)

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(cryptobots.router, prefix="/cryptobots", tags=["cryptobots"])
api_router.include_router(binance_account.router, prefix="/binance/accounts", tags=["binance_accounts"])
api_router.include_router(telegram.router, prefix="/telegram", tags=["telegrams"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
