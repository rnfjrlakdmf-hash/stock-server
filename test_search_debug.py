import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from korea_data import search_korean_stock_symbol, get_korean_name

test_keywords = ["한화오션", "에코프로", "삼성전자", "카카오", "NAVER", "하이브"]

print("Starting Search Validation...")
for kw in test_keywords:
    print(f"\nSearching for: {kw}")
    try:
        symbol = search_korean_stock_symbol(kw)
        print(f" -> Result Symbol: {symbol}")
        
        if symbol:
            name = get_korean_name(symbol + ".KS") # Try KS
            if not name:
                name = get_korean_name(symbol + ".KQ") # Try KQ
            print(f" -> Resolved Name: {name}")
        else:
            print(" -> FAILED to find symbol")
            
    except Exception as e:
        print(f" -> ERROR: {e}")
