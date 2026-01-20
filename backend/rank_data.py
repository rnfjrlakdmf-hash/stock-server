import yfinance as yf

from concurrent.futures import ThreadPoolExecutor

# 캐싱을 위한 전역 변수 (간단한 인메모리 캐시)
CACHE_TOP10 = {
    "KR": {"data": [], "timestamp": 0},
    "US": {"data": [], "timestamp": 0}
}
CACHE_DURATION = 15  # 15초

def get_realtime_top10(market="KR", refresh=False):
    """
    KOSPI(국내) 및 S&P500(미국) 시가총액 상위 10개 실시간 시세 조회
    market: 'KR' or 'US'
    refresh: True면 캐시 무시하고 강제 업데이트
    """
    global CACHE_TOP10
    import time
    
    current_time = time.time()
    # refresh가 아니고 데이터가 있으면 즉시 반환 (속도 최적화)
    if not refresh and market in CACHE_TOP10 and CACHE_TOP10[market].get("data"):
        return CACHE_TOP10[market]["data"]

    # 1. 종목 리스트 확보
    symbols = []
    
    if market == "KR":
        # 네이버 금융 등에서 크롤링하거나 고정 리스트 사용
        # 안정성을 위해 주요 대형주 고정 리스트 사용 (유지보수 용이)
        # 삼성전자, SK하이닉스, LG에너지솔루션, 삼성바이오로직스, 현대차, 기아, 셀트리온, KB금융, POSCO홀딩스, NAVER
        # 코스피 시총 상위 10 (2024 기준)
        symbols = [
            {"ticker": "005930.KS", "name": "삼성전자"},
            {"ticker": "000660.KS", "name": "SK하이닉스"},
            {"ticker": "373220.KS", "name": "LG에너지솔루션"},
            {"ticker": "207940.KS", "name": "삼성바이오로직스"},
            {"ticker": "005380.KS", "name": "현대차"},
            {"ticker": "000270.KS", "name": "기아"},
            {"ticker": "068270.KS", "name": "셀트리온"},
            {"ticker": "105560.KS", "name": "KB금융"},
            {"ticker": "005490.KS", "name": "POSCO홀딩스"},
            {"ticker": "035420.KS", "name": "NAVER"}
        ]
        
    elif market == "US":
        # 미국 대형 기술주 위주 (S&P 500 Top)
        symbols = [
            {"ticker": "AAPL", "name": "Apple"},
            {"ticker": "MSFT", "name": "Microsoft"},
            {"ticker": "NVDA", "name": "NVIDIA"},
            {"ticker": "GOOGL", "name": "Alphabet (Google)"},
            {"ticker": "AMZN", "name": "Amazon"},
            {"ticker": "META", "name": "Meta"},
            {"ticker": "TSLA", "name": "Tesla"},
            {"ticker": "BRK-B", "name": "Berkshire Hathaway"},
            {"ticker": "LLY", "name": "Eli Lilly"},
            {"ticker": "AVGO", "name": "Broadcom"}
        ]
    
    # 2. 병렬로 데이터 가져오기 (속도 개선)
    results = []
    
    # [New] 통합 데이터 조회 함수 사용 (네이버 우선 -> yfinance Fallback)
    from stock_data import get_simple_quote

    def fetch_data(item):
        try:
            ticker = item['ticker']
            
            # get_simple_quote는 {"price": "75,000", "change": "+500", "change_percent": "+0.67%"} 형태 반환
            quote = get_simple_quote(ticker)
            
            if quote and quote.get("price") != "0" and quote.get("price") != "-":
                # 문자열 데이터를 float로 변환 (계산 및 정렬 용도)
                try:
                    price_str = str(quote["price"]).replace(",", "").replace("₩", "").replace("$", "")
                    price = float(price_str)
                    
                    # Fix: quote['change'] contains the percentage string (e.g. "+0.47%")
                    # quote['change_percent'] is missing in simple quotes
                    
                    raw_change = str(quote["change"]).replace(",", "").replace("+", "").replace("▲", "").replace("▼", "").replace("%", "")
                    val = float(raw_change)
                    
                    if str(quote["change"]).startswith("-") or "▼" in str(quote["change"]):
                        val = -abs(val)
                        
                    # Assign parsed percentage to both fields logic
                    change_pct = val
                    
                    # Calculate estimated absolute change for compatibility
                    # Absolute Change = Price * (Percent / 100)
                    change = price * (change_pct / 100.0)

                except Exception as e:
                    # Parsing failed, default to 0
                    # print(f"Warning: Parsing error for {ticker}: {e}")
                    price = 0.0
                    change = 0.0
                    change_pct = 0.0
            else:
                # 완전 실패 시
                # print(f"Warning: No valid quote for {ticker}. Quote: {quote}")
                price = 0.0
                change = 0.0
                change_pct = 0.0
            
            return {
                "rank": 0, 
                "symbol": item['ticker'],
                "name": item['name'],
                "price": price,
                "change": change,
                "change_percent": change_pct
            }
        except Exception as e:
            # 에러 로그 출력 (디버깅용)
            # print(f"Error fetching {item['ticker']}: {e}")
            return {
                "rank": 0, 
                "symbol": item['ticker'],
                "name": item['name'],
                "price": 0.0,
                "change": 0.0,
                "change_percent": 0.0
            }

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(fetch_data, item) for item in symbols]
        for future in futures:
            try:
                # 타임아웃 3초로 조금 여유있게
                res = future.result(timeout=3)
                if res:
                    results.append(res)
            except Exception as e:
                print(f"Fetch thread error or timeout: {e}")
    
    # 3. 시가총액 순이 아닐 수 있으므로 (미국장은 순동이 심함), 가격순? 아니면 고정 리스트 순서대로?
    # 요청은 "1위부터 10위까지" 이므로 시가총액 데이터를 같이 가져와서 정렬하면 좋겠지만, 
    # fast_info에는 market_cap이 정확치 않을 수 있음. 
    # 여기서는 "주요 종목 Top 10"으로 정의하고, 입력된 순서(대략적 시총순)를 유지하여 랭킹 부여
    # 단, 미국 주식 리스트는 수시로 바뀔 수 있음. 일단 위 고정 리스트 순서대로 랭크 부여.
    
    # 결과 순서 맞추기 (입력 리스트 순서대로)
    # (병렬 처리로 순서 섞일 수 있으므로 매핑 필요)
    
    # 3. 결과 매핑 및 랭킹 부여 (데이터가 없어도 리스트는 유지하여 프론트엔드 에러 방지)
    final_list = []
    
    # 결과를 딕셔너리로 변환하여 찾기 쉽게 함
    results_map = {r['symbol']: r for r in results}
    
    rank = 1
    for item in symbols:
        ticker_symbol = item['ticker']
        
        if ticker_symbol in results_map:
            # 데이터 성공적으로 가져옴
            data = results_map[ticker_symbol]
            data['rank'] = rank
            final_list.append(data)
        else:
            # 실패 시 Fallback 데이터 생성 (화면에라도 표시되게)
            final_list.append({
                "rank": rank,
                "symbol": ticker_symbol,
                "name": item['name'],
                "price": 0.0,
                "change": 0.0,
                "change_percent": 0.0
            })
        rank += 1
            
    if final_list:
        CACHE_TOP10[market] = {
            "data": final_list,
            "timestamp": current_time
        }
            
    return final_list

if __name__ == "__main__":
    # Test
    print("KR:", get_realtime_top10("KR"))
    print("US:", get_realtime_top10("US"))
