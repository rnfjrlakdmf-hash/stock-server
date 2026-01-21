
import requests
from bs4 import BeautifulSoup

def test_sise_access():
    # KOSPI Top stocks
    url = "https://finance.naver.com/sise/sise_market_sum.naver?sosok=0&page=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91"
    }
    
    print(f"Testing URL: {url}")
    try:
        res = requests.get(url, headers=headers)
        print(f"Status Code: {res.status_code}")
        
        # Decode
        res.encoding = res.apparent_encoding
        
        if "일시적 오류" in res.text:
            print("Blocked (Error page)")
        else:
            soup = BeautifulSoup(res.text, 'html.parser')
            # Look for stock links
            links = soup.select("table.type_2 tbody tr td a.tltle")
            print(f"Found {len(links)} stocks on page 1.")
            for link in links[:5]:
                print(f"{link.text} -> {link['href']}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_sise_access()
