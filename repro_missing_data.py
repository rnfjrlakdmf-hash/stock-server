
import sys
import os

# Add backend directory to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from korea_data import get_naver_daily_prices, get_naver_stock_info
from stock_data import get_stock_info
import json

def test_korean_stock_fetch(symbol):
    print(f"Testing fetch for {symbol}...")
    
    # 1. Test get_naver_daily_prices directly
    print("\n[Direct] get_naver_daily_prices:")
    try:
        daily_prices = get_naver_daily_prices(symbol)
        print(f"Daily Prices Count: {len(daily_prices)}")
        if daily_prices:
            print(f"First Item: {daily_prices[0]}")
    except Exception as e:
        print(f"Error in get_naver_daily_prices: {e}")

    # 2. Test get_stock_info (high level)
    print("\n[High Level] get_stock_info:")
    try:
        info = get_stock_info(symbol)
        if info:
            print(f"Name: {info.get('name')}")
            print(f"Price: {info.get('price')}")
            print(f"News Count: {len(info.get('news', []))}")
            if info.get('news'):
                 print(f"First News: {info.get('news')[0]}")
            else:
                 print("News is empty.")
                 
            print(f"Daily Prices Count: {len(info.get('daily_prices', []))}")
        else:
            print("get_stock_info returned None")
    except Exception as e:
        print(f"Error in get_stock_info: {e}")

if __name__ == "__main__":
    test_korean_stock_fetch("005930.KS") # Samsung Electronics
