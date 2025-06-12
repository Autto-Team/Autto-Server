import requests
import os
from pykis import KisAccount, PyKis, KisBalance, KisOrder, KisStock

kis = PyKis("secret.json", keep_token=True)

account: KisAccount = kis.account()

balance: KisBalance = account.balance()

good_stock = '{ "GOOD PEOPLE CO., LTD." : "033340", "DOZN INC." : "462860", "DONGYANG STEEL PIPE" : "008970" }'

# hanchang: KisStock = kis.stock("005110")

# order: KisOrder = hanchang.buy(price=480, qty=3)

# API 키 설정
api_key = os.getenv("XAI_API_KEY")
if not api_key:
    api_key = "xai-7rXAQxektVAGrxTsZNdE3Q1WCIdFahUs94UPmfkF7SmGuufyMceLZgEJprycYbiNjmLPsbnDeVZQ06dK"  # 실제 API 키로 교체 (xAI Developer Console에서 발급)

# API 엔드포인트
url = "https://api.x.ai/v1/chat/completions"  # 올바른 엔드포인트

# 요청 헤더
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# DeepSearch 요청 본문
payload = {
    "model": "grok-3",
    "messages": [
        {
            "role": "system",
            "content": "내 정보는 : " + str(balance) + "이고 " + good_stock + " 해당 종목들 중에서 거래를 진행함에 있어 가장 큰 이익을 볼 가능성이 있는 주식 1개를 선택하고 판매와 추가 구매를 직접 판단해."
        },
        {
            "role": "user",
            "content": "선택된 주식의 동향을 파악해서 구매 or 판매를 결정해. 부가 설명은 절대 포함시키지 말고 구매할 종목과 네가 정한 적절한 지정가, 수량을 딕셔너리 Json 형식으로 응답해. { orderType: buy, stock_code: XXXXXX, price: XXXX, qty: XX } 형식으로"
        }
    ],
    "max_tokens": 20,
    "temperature": 0.7
}

# API 요청 보내기
try:
    response = requests.post(url, headers=headers, json=payload)

    # 응답 처리
    if response.status_code == 200:
        result = response.json()
        print(result["choices"][0]["message"]["content"])
    else:
        print(f"에러 발생: {response.status_code}, {response.text}")

except Exception as e:
    print(f"요청 실패: {str(e)}")