from datetime import date
from pykis import PyKis, KisAccount, KisDailyOrders

def get_trading_records():
    kis = PyKis("../config/KoreaInvest.json", keep_token=True)

    account: KisAccount = kis.account()
    daily_orders: KisDailyOrders = account.daily_orders(start=date(2024, 1, 1), end=date(2025, 6, 19))

    order_summary = []

    for order in daily_orders.orders:
        try:
            stock_name = kis.stock(order.order_number.name).name
        except Exception as e:
            stock_name = f"{order.order_number.name}"

        order_summary.append({
            "name": stock_name,
            "type": order.type,
            "price": int(order.price),
            "qty": order.qty,
            "executed_qty": order.executed_qty
        })

    return order_summary
