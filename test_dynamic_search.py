
import sys
import os
import time

# Add backend directory to path
sys.path.append(os.path.abspath("backend"))

from korea_data import search_korean_stock_symbol, DYNAMIC_STOCK_MAP

def test_dynamic_search():
    print("Waiting for background indexing (5 seconds)...")
    time.sleep(5) # Wait for thread to run
    
    print(f"Dynamic Map Size: {len(DYNAMIC_STOCK_MAP)}")
    
    test_cases = ["안랩", "카카오페이", "제주항공"]
    
    for tc in test_cases:
        print(f"Searching for: {tc}")
        symbol = search_korean_stock_symbol(tc)
        print(f"Result for {tc}: {symbol}")
        
    if len(DYNAMIC_STOCK_MAP) > 100:
        print("Indexing seems successful.")

if __name__ == "__main__":
    test_dynamic_search()
