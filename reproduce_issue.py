
import sys
import os

# Add backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from stock_data import get_stock_info

def test_search(symbol):
    print(f"Testing search for: {symbol}")
    try:
        result = get_stock_info(symbol)
        if result:
            print("Success!")
            print(f"Name: {result.get('name')}")
            print(f"Price: {result.get('price')}")
        else:
            print("Failed: No result returned")
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Test valid Korean stock code
    test_search("005930")
    
    # Test valid Korean stock code with .KS
    test_search("005930.KS")

    # Test valid US stock code
    test_search("AAPL")
