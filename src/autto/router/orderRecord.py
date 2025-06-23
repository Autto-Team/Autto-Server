from fastapi import APIRouter

from src.autto.service.orderRecordService import get_trading_records

router = APIRouter()

router.get("/records")
async def tradingrecords():
    get_trading_records()
