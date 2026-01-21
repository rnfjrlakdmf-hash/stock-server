
import sys
import os

# Add backend directory to sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from korea_data import search_korean_stock_symbol

def test_search(keyword):
    print(f"Searching for: {keyword}")
    result = search_korean_stock_symbol(keyword)
    print(f"Result for '{keyword}': {result}")

if __name__ == "__main__":
    test_search("삼성중공업")
    test_search("카카오")
    test_search("UnknownStockName123")
