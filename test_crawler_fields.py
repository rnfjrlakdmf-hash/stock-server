
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from korea_data import get_naver_stock_info

def test_crawl():
    print("Testing Updated Crawler for Samsung Electronics (005930)...")
    info = get_naver_stock_info("005930")
    
    if not info:
        print("Failed to fetch info.")
        return

    print(f"Name: {info.get('name')}")
    print(f"Volume: {info.get('volume')} (Expected > 0)")
    print(f"Open: {info.get('open')}")
    print(f"High: {info.get('day_high')}")
    print(f"Low: {info.get('day_low')}")
    print(f"52 High: {info.get('year_high')}")
    print(f"52 Low: {info.get('year_low')}")
    print(f"Forward PE: {info.get('forward_pe')}")
    print(f"Forward EPS: {info.get('forward_eps')}")
    print(f"BPS: {info.get('bps')}")
    print(f"DPS: {info.get('dividend_rate')}")
    print(f"Yield: {info.get('dvr')}")
    
if __name__ == "__main__":
    test_crawl()
