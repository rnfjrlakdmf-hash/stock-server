
import sys
import os
# Add backend directory to sys.path
sys.path.append(os.path.join(os.getcwd(), "backend"))

try:
    from main import read_stock
except ImportError:
    # If running from root, maybe need to change dir context or adjust path further
    # Let's try changing CWD to backend
    os.chdir("backend")
    sys.path.append(os.getcwd())
    from main import read_stock

import traceback

def test():
    print("--- Starting Test ---")
    symbol = "005930" # Samsung Electronics
    print(f"Testing read_stock('{symbol}') with skip_ai=True...")
    
    try:
        result = read_stock(symbol, skip_ai=True)
        print("Function returned:", result)
        
        if result.get("status") == "success":
            print("SUCCESS: Data found.")
        else:
            print("FAILURE: API returned error status.")
            
    except Exception as e:
        print("CRITICAL EXCEPTION during execution:")
        traceback.print_exc()

if __name__ == "__main__":
    test()
