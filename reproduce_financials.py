
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from korea_data import get_naver_stock_info

symbol = "005930.KS"
print(f"Fetching info for {symbol}...")
info = get_naver_stock_info(symbol)

if info:
    print("--- Financials ---")
    print(f"PER: {info.get('per')}")
    print(f"EPS: {info.get('eps')}")
    print(f"PBR: {info.get('pbr')}")
    print(f"Dividend Yield: {info.get('dvr')}")
    print(f"Forward PER: {info.get('forward_pe')}")
    print(f"Forward EPS: {info.get('forward_eps')}")
    print(f"BPS: {info.get('bps')}")
    print(f"Dividend Rate: {info.get('dividend_rate')}")
    print(f"Year High/Low: {info.get('year_high')} / {info.get('year_low')}")
    print(f"Open: {info.get('open')}")
else:
    print("Failed to fetch info.")
