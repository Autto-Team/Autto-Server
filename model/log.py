from sqlmodel import SQLModel, create_engine, Field
from typing import Optional
from datetime import datetime

DATABASE_URL = "postgresql://postgres:3141@localhost:5432/autto"
engine = create_engine(DATABASE_URL, echo=True)

class Stock(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key = True)
    stock_code: str
    buy_amount: int
    sell_amount: int
    rate: float
    total_money: int
    date: Optional[datetime] = Field(default_factory = datetime.now)


def init_db():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()