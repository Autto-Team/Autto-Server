from random import choice

from openai import OpenAI
from pykis import PyKis, KisAuth, KisAccount, KisBalance
import json, requests, ast

kis = PyKis(KisAuth.load('../config/KoreaInvest.json'), keep_token=True)

with open('../config/XAI.json', 'r') as f:
    xai_config = json.load(f)

# print(xai_config['XAI_API_KEY'])


api_key = xai_config['api_key']

# client = OpenAI(
#     api_key=api_key,
#     base_url=xai_config['DEEPSEARCH_BASE_URL'],
# )

time_check = 0 # 나중에 시간으로 확인

if time_check == 0:
    time_check = "한국"
else:
    time_check = "미국"


account: KisAccount = kis.account()
balance: KisBalance = account.balance()
money = balance.withdrawable_amount

print(money)


url = "https://api.x.ai/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + api_key
}
payload = {
    "messages": [
        {
            "role": "system",
            "content": f"너는 {time_check} 주식 시장 전문가야. 사용자의 요청에 따라 {str(money)}원 자금으로 하루 1% 수익을 목표로, 현재 거래량이 충분히 뒷받침되는 단타 매매에 적합한 한국 주식을 신중히 분석해. 응답은 반드시 {{ 'stock_name1': code, 'stock_name2': code, 'stock_name3': code }} 형태의 딕셔너리만 반환하고, 어떤 설명이나 추가 정보도 포함시키지 마."
        },
        {
            "role": "user",
            "content": f"DeepSearch 기능으로 현재 자금 {str(money)}원으로 하루 1% 수익을 목표로 지금 현재 거래량이 뒷받침되는 단타 매매에 적합한 한국 주식을 신중히 분석해, 주식의 자세한 그래프를 잘 보고 판단해서. 주식 이름과 종목 코드 3개만 딕셔너리 형태로 제공해. {{ 'stock_name1': code, 'stock_name2': code, 'stock_name3': code }} 이런 형식으로"
        }
    ],
    "search_parameters" : {
        "mode" : "on",
    },
    "model" : "grok-3-latest",

}
response = requests.post(url, headers=headers, json=payload)

# response = "{'id': '97008ea0-b3f7-4fea-a1d8-91232aaf5cf8', 'object': 'chat.completion', 'created': 1749445083, 'model': 'grok-3', 'choices': [{'index': 0, 'message': {'role': 'assistant', 'content': "{\n    '삼성전자': '005930',\n    '카카오': '035720',\n    '현대차': '005380'\n}", 'refusal': None}, 'finish_reason': 'stop'}], 'usage': {'prompt_tokens': 3857, 'completion_tokens': 32, 'total_tokens': 3889, 'prompt_tokens_details': {'text_tokens': 3857, 'audio_tokens': 0, 'image_tokens': 0, 'cached_tokens': 142}, 'completion_tokens_details': {'reasoning_tokens': 0, 'audio_tokens': 0, 'accepted_prediction_tokens': 0, 'rejected_prediction_tokens': 0}, 'num_sources_used': 3}, 'system_fingerprint': 'fp_d8d6e9f7d0', 'citations': ['https://ddshop.tistory.com/entry/2025%EB%85%84-3%EC%9B%94-4%EC%9D%BC-%ED%95%9C%EA%B5%AD-%EC%A3%BC%EC%8B%9D-%EC%8B%9C%EC%9E%A5-%EA%B1%B0%EB%9E%98%EB%9F%89-Top-5-%EC%99%84%EB%B2%BD-%EB%B6%84%EC%84%9D', 'https://biz.chosun.com/stock/stock_general/2025/06/05/BK6HNBXMZYWLSLA65KZ5CUUR4Q/', 'https://ko.tradingeconomics.com/united-states/stock-market', 'https://ko.tradingeconomics.com/south-korea/stock-market', 'https://www.onestepblog.info/2025/05/6.html?m=1', 'https://finance.yahoo.com/news/m-estate-planner-6-things-210110452.html', 'https://ca.finance.yahoo.com/news/film-festival-showcases-artificial-intelligence-153443137.html', 'https://www.espn.com/nba/story/_/id/45466074/nba-finals-2025-how-thunder-avoid-2-0-deficit-pacers', 'https://finance.yahoo.com/personal-finance/mortgages/article/mortgage-refinance-rates-today-saturday-june-7-2025-100051609.html', 'https://www.businessinsider.com/pride-month-companies-brands-pullback-2025-6', 'https://x.com/heoilikj/status/1926643031152677280', 'https://x.com/heoilikj/status/1921554067182211455', 'https://x.com/jesselivrmore/status/1870349203505090837', 'https://x.com/jesselivrmore/status/1915380287003123891', 'https://x.com/dons_korea/status/1898521949397234165']}"

# response_dict = ast.literal_eval(response)

print(response.json())



# completion = client.chat.completions.create(
#     model = "grok-3",
#     messages = [
#     {
#         "role": "system",
#         "content": f"너는 {time_check} 주식 시장 전문가야. 사용자의 요청에 따라 {str(money)}원 자금으로 하루 1% 수익을 목표로, 현재 거래량이 충분히 뒷받침되는 단타 매매에 적합한 한국 주식을 신중히 분석해. 응답은 반드시 {{ 'stock_name1': code, 'stock_name2': code, 'stock_name3': code }} 형태의 딕셔너리만 반환하고, 어떤 설명이나 추가 정보도 포함시키지 마."
#     },
#     {
#         "role": "user",
#         "content": f"현재 자금 {str(money)}원으로 하루 1% 수익을 목표로 지금 현재 거래량이 뒷받침되는 단타 매매에 적합한 한국 주식을 신중히 분석해, 주식 이름과 종목 코드 3개만 딕셔너리 형태로 제공해. {{ 'stock_name1': code, 'stock_name2': code, 'stock_name3': code }} 이런 형식으로"
#     }
#     ],
#
# )
#
# print(completion)

# client = OpenAI(
#   api_key="<YOUR_XAI_API_KEY_HERE>",
#   base_url="https://api.x.ai/v1",
# )
#
# completion = client.chat.completions.create(
#   model="grok-3",
#   messages=[
#     {"role": "system", "content": "You are a PhD-level mathematician."},
#     {"role": "user", "content": "What is 2 + 2?"},
#   ],
# )
#
# print(completion.choices[0].message)
#
# ""


'''현재 자금 200,000원으로 하루 1% 수익을 목표로 지금 현재 거래량이 뒷바침되는 단타 매매에 적합한 한국 주식을 신중히 분석해, 주식 이름과 종목 코드 3개만 딕셔너리 형태로 제공해. 다른 설명이나 주의점은 포함시키지 마 무조건 디셔너리만 보내줘. { "stock_name1" : code, "stock_name2" : code, "stock_name3" : code, } 이런 형식으로'''