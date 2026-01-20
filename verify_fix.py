
import requests
import time
import sys
import threading
import uvicorn
from contextlib import contextmanager

# Add path to backend to import modules
import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from backend.stock_data import get_stock_info

def test_search_logic():
    print("Testing Search Logic for '카카오' (Expected: 035720)...")
    
    # Direct call to get_stock_info (simulating API controller)
    try:
        data = get_stock_info("카카오", skip_ai=True)
        if data and "035720" in data.get("symbol", ""):
            print("SUCCESS: Found '카카오' ->", data["symbol"])
            # Check price presence
            if data.get("price") and data["price"] != "0":
                print(f"Price: {data['price']}")
                return True
            else:
                print("WARNING: Price missing or 0")
        else:
            print("FAILURE: Did not find '035720' for '카카오'")
            print("Response:", data)
            return False
            
    except Exception as e:
        print(f"EXCEPTION: {e}")
        return False

if __name__ == "__main__":
    success = test_search_logic()
    if success:
        print("TEST PASSED")
        sys.exit(0)
    else:
        print("TEST FAILED")
        sys.exit(1)
