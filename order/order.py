import mojito
import json, requests

with open('../config/KoreaInvest.json', 'r') as file:
    config = json.load(file)

with open('../config/XAI.json', 'r') as f:
    xai_config = json.load(f)


api_key = xai_config['api_key']


broker = mojito.KoreaInvestment(
    api_key = config['appkey'],
    api_secret = config['secretkey'],
    acc_no = config['account'],
)

balance = broker.fetch_balance()

good_stock = '''{
    "MR. BLUE CORPORATION": "207760",
    "FINGER STORY CO., LTD.": "417180",
    "ILSHIN STONE": "007110"
}'''

system_from = "내 정보는 : " + str(balance) + "이고 " + good_stock + " 해당 종목들 중에서 거래를 진행함에 있어 가장 큰 이익을 볼 가능성이 있는 주식 1개를 선택하고 판매와 추가 구매를 직접 판단해."
user_from = "선택된 주식의 동향을 파악해서 구매 or 판매를 결정해. 부가 설명은 절대 포함시키지 말고 구매할 종목과 네가 정한 적절한 지정가, 수량을 딕셔너리 Json 형식으로 응답해. { orderType: buy, stock_code: XXXXXX, price: XXXX, qty: XX } 형식으로"

url = "https://api.x.ai/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + api_key
}
payload = {
    "messages": [
    {
        "role": "system",
        "content": f"{system_from}"
    },
    {
        "role": "user",
        "content": f"{user_from}"
    }
    ],
    "search_parameters" : {
        "mode" : "on",
    },
    "model" : "grok-3",
}

print(payload)

response = requests.post(url, headers=headers, json=payload)


data = response.json()

print(data)

# data =  {'id': '06262483-5f4b-448b-9249-8a4467067725', 'object': 'chat.completion', 'created': 1749522294, 'model': 'grok-3', 'choices': [{'index': 0, 'message': {'role': 'assistant', 'content': '{\n    "orderType": "buy",\n    "stock_code": "207760",\n    "price": 5000,\n    "qty": 10\n}', 'refusal': None}, 'finish_reason': 'stop'}], 'usage': {'prompt_tokens': 2842, 'completion_tokens': 34, 'total_tokens': 2876, 'prompt_tokens_details': {'text_tokens': 2842, 'audio_tokens': 0, 'image_tokens': 0, 'cached_tokens': 376}, 'completion_tokens_details': {'reasoning_tokens': 0, 'audio_tokens': 0, 'accepted_prediction_tokens': 0, 'rejected_prediction_tokens': 0}, 'num_sources_used': 3}, 'system_fingerprint': 'fp_d8d6e9f7d0', 'citations': ['https://www.investing.com/equities/mr-blue-corp', 'https://ca.investing.com/equities/mr-blue-corp', 'https://finance.yahoo.com/quote/207760.KQ/', 'https://www.bloomberg.com/quote/207760:KS', 'https://www.defenseworld.net/2025/06/07/nuveen-asset-management-llc-decreases-stock-position-in-bluebird-bio-inc-nasdaqblue.html', 'https://financialpost.com/pmn/business-pmn/traders-scour-for-elusive-catalyst-to-push-sp-500-to-record', 'https://finance.yahoo.com/news/live/stock-market-today-sp-500-hits-6000-as-tesla-rebounds-amid-trump-musk-feud-cooldown-200103501.html', 'https://www.geneonline.com/regeneron-licenses-weight-loss-drug-and-shares-data-on-muscle-preservation-medicines-as-bluebird-bio-goes-private/', 'https://www.cnyhomepage.com/business/press-releases/cision/20250606NY04906/spencer-trask-co-nets-public-stake-in-circle-internet-group-at-nyse-debut', 'https://x.com/SrPetersETH/status/1816817213707342163', 'https://x.com/DeItaone/status/1792478493558685829', 'https://x.com/matteodotsui/status/1869429912874168638', 'https://x.com/Shivanishrma83/status/1912445616501801334', 'https://x.com/dougboneparth/status/1874838154282414308']}
#

message_content = data['choices'][0]['message']['content']

dic = json.loads(message_content)


# Grok DeepSearch 이슈가 좀 심각하다....
dic["qty"] = 1
dic['price'] = 0

print(dic)

broker.create_market_buy_order(
    symbol=dic['stock_code'],
    quantity=dic['qty']
)

print(broker.fetch_balance())
