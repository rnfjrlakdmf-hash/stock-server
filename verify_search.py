import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from stock_data import get_stock_info

def verify_stock(symbol, expected_name_part=None, expected_currency=None, check_krw=False):
    print(f"\n--- Verifying {symbol} ---")
    data = get_stock_info(symbol, skip_ai=True)
    
    if not data:
        print(f"❌ Failed to fetch data for {symbol}")
        return
    
    print(f"✅ Name: {data.get('name')}")
    print(f"✅ Symbol: {data.get('symbol')}")
    print(f"✅ Currency: {data.get('currency')}")
    print(f"✅ Price: {data.get('price')}")
    
    if check_krw:
        print(f"✅ Price KRW: {data.get('price_krw')}")
        if not data.get('price_krw'):
            print("❌ Price KRW missing for global stock!")

    if expected_name_part and expected_name_part not in data.get('name', ''):
         print(f"⚠️ Warning: Name does not contain '{expected_name_part}'")

    if expected_currency and data.get('currency') != expected_currency:
         print(f"❌ Currency Mismatch: Expected {expected_currency}, Got {data.get('currency')}")

print("Starting Verification...")

# 1. Global Stock
verify_stock("AAPL", "애플", "USD", check_krw=True)
verify_stock("TSLA", "테슬라", "USD", check_krw=True)

# 2. KOSDAQ Stock (English Search -> Mapped to .KQ)
# Note: frontend maps 'ECOPRO' -> '086520.KQ' but here we test the backend receiving the mapped symbol or raw code
verify_stock("086520.KQ", "에코프로", "KRW")

# 3. KOSDAQ Stock (Raw Code -> Auto Detect)
# If we pass '086520', backend should try KS/KQ and find KQ
verify_stock("086520", "에코프로", "KRW")

print("\nVerification Complete.")
