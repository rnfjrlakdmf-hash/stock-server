
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from stock_data import get_stock_info

def test_search(symbol):
    print(f"\n--- Testing Search for: {symbol} ---")
    try:
        result = get_stock_info(symbol)
        if result:
            print(f"Success: Found {result['name']} ({result['symbol']})")
            print(f"Price: {result['price']}")
        else:
            print("Failed: Result is None")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Test cases
    targets = ["005930", "035420", "AAPL", "NVDA", "INVALID123"]
    
    for t in targets:
        test_search(t)
