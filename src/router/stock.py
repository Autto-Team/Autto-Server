from fastapi import APIRouter

from src.service.stockService import get_my_stock_info, get_profit_rate

router = APIRouter()

router.get("/stocks")
async def mystocks():
    get_my_stock_info()

router.get("/rates")
async def myrate():
    get_profit_rate()
