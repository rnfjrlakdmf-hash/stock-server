
from backend.stock_data import get_stock_info
import json

symbol = "005930.KS"
print(f"Testing {symbol}...")
try:
    data = get_stock_info(symbol)
    if data:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print("No data returned")
except Exception as e:
    print(f"Error: {e}")
