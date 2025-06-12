import requests
from pykis import PyKis, KisAuth
import logging
import time
import json

logging.basicConfig(filename="data/logs/data.log", level=logging.INFO)


def get_top_volume_stocks(market="KR", limit=10):
    """
    한국 또는 미국 시장에서 거래량 상위 종목을 KIS API로 조회합니다.

    Args:
        market (str): 'KR' (한국) 또는 'US' (미국)
        limit (int): 반환할 종목 수

    Returns:
        list: [{'symbol': str, 'name': str, 'volume': int}] 형식의 리스트
    """
    # Step 1: PyKis 초기화
    try:
        auth = KisAuth.load('../../config/KoreaInvest.json')
        kis = PyKis(auth, keep_token=True)
    except Exception as e:
        logging.error(f"Failed to initialize PyKis: {e}")
        raise

    # Step 2: KIS API 엔드포인트 설정
    if market == "KR":
        url = "https://openapi.koreainvestment.com:9443/uapi/domestic-stock/v1/quotations/inquire-ccnl"
        tr_id = "FHKST01010400"
        params = {
            "fid_cond_mrkt_div_code": "J",  # 주식
            "fid_input_iscd": "0001",  # 전체 종목
            "fid_rank_sort_cls_code": "0",  # 거래량 순
            "fid_trad_dt": "",  # 거래일 (빈 문자열: 당일)
            "fid_hour_cls_code": "0",  # 전체 시간
            "fid_input_cnt": str(limit)  # 출력 건수
        }
    elif market == "US":
        url = "https://openapi.koreainvestment.com:9443/uapi/overseas-price/v1/quotations/inquire-ccnl"
        tr_id = "HHDFS76950200"
        params = {
            "AUTH": "",  # 빈 문자열
            "EXCD": "NASD",  # NASDAQ (NYSE의 경우 'NYS')
            "SYMB": "",  # 전체 종목
            "GUBN": "0",  # 전체
            "BYMD": "",  # 거래일 (빈 문자열: 당일)
            "CNT": str(limit)  # 출력 건수
        }
    else:
        raise ValueError("Unsupported market. Use 'KR' or 'US'.")

    # Step 3: KIS API 호출 (PyKis rest.get 사용)
    try:
        headers = {
            "authorization": f"Bearer {kis.auth.token}",
            "appkey": auth.appkey,
            "appsecret": auth.secretkey,
            "tr_id": tr_id,
            "custtype": "P"  # 개인
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        # Step 4: 응답 데이터 파싱
        volumes = []
        if market == "KR":
            for item in data.get("output", []):
                volumes.append({
                    "symbol": item["stck_shrn_iscd"],
                    "name": item["stck_name"],
                    "volume": int(item["acml_vol"])
                })
        else:  # US
            for item in data.get("output", []):
                volumes.append({
                    "symbol": item["symb"],
                    "name": item["name"],
                    "volume": int(item["acml_vol"])
                })

        # Step 5: 거래량 기준 정렬 및 상위 N개 선택
        sorted_volumes = sorted(volumes, key=lambda x: x['volume'], reverse=True)[:limit]

        # Step 6: 결과 로깅 및 반환
        logging.info(f"Top {limit} stocks for {market}: {sorted_volumes}")
        return sorted_volumes

    except Exception as e:
        logging.error(f"Error fetching data from KIS API: {e}")
        raise

    finally:
        time.sleep(0.2)  # API 호출 제한 준수


if __name__ == "__main__":
    try:
        top_stocks_kr = get_top_volume_stocks(market="KR", limit=5)
        print("Korea Top Stocks:", top_stocks_kr)
        top_stocks_us = get_top_volume_stocks(market="US", limit=5)
        print("US Top Stocks:", top_stocks_us)
    except Exception as e:
        print(f"Error: {e}")