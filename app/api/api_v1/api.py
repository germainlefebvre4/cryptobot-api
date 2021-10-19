from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    cryptobots, login, utils, binance_account, telegram,
    users,
    metrics
)
from app.api.api_v1.private import (
    users as users_private,
    binance_account as binance_account_private,
)


api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(cryptobots.router, prefix="/cryptobots", tags=["cryptobots"])
api_router.include_router(binance_account.router, prefix="/binance/accounts", tags=["binance_accounts"])
api_router.include_router(telegram.router, prefix="/telegram", tags=["telegrams"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])

api_router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])


api_router_private = APIRouter()
api_router_private.include_router(users_private.router, prefix="/users", tags=["private"])
api_router_private.include_router(binance_account_private.router, prefix="/binance/accounts", tags=["private"])
