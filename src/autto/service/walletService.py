from pykis import PyKis, KisBalance, KisAccount

def get_wallet_info():
    kis = PyKis("../config/KoreaInvest.json", keep_token=True)

    account: KisAccount = kis.account()

    balance: KisBalance = account.balance()

    myBalance = balance.withdrawable_amount

    formatted_amount = f"{myBalance:,.0f} KRW"

    print(formatted_amount)

    return {
        "myBalance": formatted_amount
    }
