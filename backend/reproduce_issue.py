
import sys
import os

# Add current directory to path so we can import modules
sys.path.append(os.getcwd())

from korea_data import get_naver_stock_info

def test_stock(symbol, name):
    print(f"Testing {name} ({symbol})...")
    try:
        data = get_naver_stock_info(symbol)
        if data:
            print(f"[SUCCESS] Found data for {symbol}")
            print(f"Name: {data.get('name')}")
            print(f"Price: {data.get('price')}")
            print(f"Market Cap: {data.get('market_cap_str')}")
            return True
        else:
            print(f"[FAILURE] get_naver_stock_info returned None for {symbol}")
            return False
    except Exception as e:
        print(f"[ERROR] Exception occurred for {symbol}: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Test Samsung Electronics covers KS
    samsung = test_stock("005930", "Samsung Electronics")
    
    # Test Ecopro covers KQ/KOSDAQ
    ecopro = test_stock("086520", "Ecopro")
    
    if not samsung or not ecopro:
        print("\nReproduction Successful: One or more stock lookups failed.")
        sys.exit(1)
    else:
        print("\nAll tests passed. Could not reproduce completely, or maybe intermittent?")
        sys.exit(0)
