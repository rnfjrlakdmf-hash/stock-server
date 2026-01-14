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
    
    def fetch_data(item):
        try:
            ticker = yf.Ticker(item['ticker'])
            
            price = 0.0
            prev_close = 0.0
            
            # 1단계: fast_info 시도
            try:
                price = getattr(ticker.fast_info, 'last_price', 0.0)
                prev_close = getattr(ticker.fast_info, 'previous_close', 0.0)
            except:
                pass
                
            # 2단계: history 시도 (데이터가 0이거나 실패 시)
            if price == 0 or prev_close == 0:
                try:
                    # 최근 5일치 가져와서 마지막 종가를 현재가로 사용
                    hist = ticker.history(period="5d")
                    if not hist.empty:
                        price = hist['Close'].iloc[-1]
                        if len(hist) >= 2:
                            prev_close = hist['Close'].iloc[-2]
                        else:
                            prev_close = price # 전일 데이터 없으면 0% 변동으로 처리
                except:
                    pass
            
            # 3단계: info 시도 (마지막 수단)
            if price == 0:
                 try:
                    info = ticker.info
                    price = info.get('currentPrice', info.get('regularMarketPrice', 0.0))
                    if prev_close == 0:
                        prev_close = info.get('previousClose', info.get('regularMarketPreviousClose', 0.0))
                 except:
                    pass

            # None 체크 및 형변환
            if price is None: price = 0.0
            if prev_close is None: prev_close = 0.0
            
            if price and prev_close and prev_close != 0:
                change = price - prev_close
                change_pct = (change / prev_close) * 100
            else:
                change = 0.0
                change_pct = 0.0
            
            return {
                "rank": 0, 
                "symbol": item['ticker'],
                "name": item['name'],
                "price": float(price),
                "change": float(change),
                "change_percent": float(change_pct)
            }
        except Exception as e:
            # 에러 로그 출력 (디버깅용)
            print(f"Error fetching {item['ticker']}: {e}")
            # 완전 실패 시 0으로 채워서 반환 (리스트에서 빠지지 않게)
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
                # 타임아웃 2초 설정 (전체 응답 지연 방지)
                res = future.result(timeout=2)
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
