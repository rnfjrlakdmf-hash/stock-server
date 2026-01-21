
import sys
import os

# Add backend directory to path
sys.path.append(os.path.abspath("backend"))

from korea_data import search_korean_stock_symbol

def test_search():
    keyword = "한화오션"
    print(f"Searching for: {keyword}")
    symbol = search_korean_stock_symbol(keyword)
    print(f"Result: {symbol}")
    
    if symbol:
        print("Success!")
    else:
        print("Failed to find symbol.")

if __name__ == "__main__":
    test_search()
