
import sys
import os
sys.path.append(os.path.abspath("backend"))

from stock_data import search_yahoo_finance

def test_yahoo():
    keywords = ["Hanwha Ocean", "한화오션", "042660.KS"]
    for k in keywords:
        print(f"Searching Yahoo for: {k}")
        res = search_yahoo_finance(k)
        print(f"Result: {res}")

if __name__ == "__main__":
    test_yahoo()
