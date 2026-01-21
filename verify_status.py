
import sys
import os
import time

# Add backend directory to path
sys.path.append(os.path.abspath("backend"))

from korea_data import search_korean_stock_symbol, DYNAMIC_STOCK_MAP
from stock_data import get_stock_info

def verify_fixes():
    print("Waiting for background indexing (3 seconds)...")
    time.sleep(3) 
    
    # 1. Check Hanwha Ocean (Manual Map or Search)
    print("\n[Test 1] Searching for '한화오션'...")
    symbol = search_korean_stock_symbol("한화오션")
    print(f"Result: {symbol}")
    
    if symbol == "042660":
        print("PASS: Hanwha Ocean found correctly.")
    else:
        print(f"FAIL: Hanwha Ocean expected 042660, got {symbol}")

    # 2. Check Samsung Electronics (Common)
    print("\n[Test 2] Searching for '삼성전자'...")
    symbol_s = search_korean_stock_symbol("삼성전자")
    print(f"Result: {symbol_s}")

    # 3. Check Global Stock Search via get_stock_info logic
    print("\n[Test 3] Fetching info for 'Tesla' (Global)...")
    # This might take a moment as it hits APIs
    info = get_stock_info("Tesla", skip_ai=True)
    if info and info['symbol'] == 'TSLA':
        print(f"PASS: Tesla found as {info['symbol']}")
    else:
        print(f"FAIL: Tesla search result: {info}")

if __name__ == "__main__":
    verify_fixes()
