from fastapi import APIRouter

from src.autto.service.walletService import get_wallet_info

router = APIRouter()

router.get("/wallet")
async def mybalance():
    get_wallet_info()