
import sys
import os

# Add backend directory to sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from korea_data import search_korean_stock_symbol
from stock_data import search_yahoo_finance

def test_search(query):
    print(f"Testing query: '{query}'")
    
    # 1. Search Naver
    naver_result = search_korean_stock_symbol(query)
    print(f"  Naver Result: {naver_result}")
    
    # 2. Search Yahoo
    yahoo_result = search_yahoo_finance(query)
    print(f"  Yahoo Result: {yahoo_result}")

if __name__ == "__main__":
    queries = [
        "삼성중공업",
        "Samsung Heavy Industries",
        "Samsung Heavy", 
        "SAMSUNGHEAVY",
        "대한항공",
        "Korean Air",
        "LG화학",
        "LG Chem",
        "Hanwha Ocean", # Formerly DSME
    ]
    
    for q in queries:
        test_search(q)
        print("-" * 20)
