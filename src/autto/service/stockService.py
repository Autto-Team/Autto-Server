from pykis import KisBalance, PyKis, KisAccount
from decimal import InvalidOperation

kis = PyKis("../config/KoreaInvest.json", keep_token=True)

account: KisAccount = kis.account()

balance: KisBalance = account.balance()

def get_my_stock_info():
    stocks = []
    for stock in balance.stocks:
        if stock.quantity == 0:
            continue

        stocks.append({
            "name": stock.name, # 주식 이름
            "quantity": int(stock.quantity), # 수량
            "amount": int(stock.amount), # 평가 금액
            "current_price": int(stock.current_price), # 현재 가격
            "purchase_price": int(stock.purchase_price), # 평균 매수 단가
            "purchase_amount": int(stock.purchase_amount), # 총 매수 금액
            "profit": int(stock.profit) # 손익 금액
        })

    return stocks

def get_profit_rate():
    profit_rate = []
    for stock in balance.stocks:
        try:
            rate = round(float(stock.profit / stock.purchase_amount * 100), 2)
        except (ZeroDivisionError, InvalidOperation):
            rate = 0.0
        profit_rate.append({
            "profit_rate": rate
        })

    return profit_rate
