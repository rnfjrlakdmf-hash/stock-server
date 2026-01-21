
import requests
from bs4 import BeautifulSoup

def test_detail_page():
    code = "042660" # Hanwha Ocean
    url = f"https://finance.naver.com/item/main.naver?code={code}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    print(f"Testing URL: {url}")
    try:
        res = requests.get(url, headers=headers)
        print(f"Status Code: {res.status_code}")
        
        # Detect encoding
        res.encoding = res.apparent_encoding
        
        if "일시적 오류로 페이지 접속이 불가합니다" in res.text:
             print("Blocked (Error content found)")
        else:
             soup = BeautifulSoup(res.text, 'html.parser')
             h2 = soup.select_one(".wrap_company h2 a")
             if h2:
                 print(f"Success! Found stock name: {h2.text}")
             else:
                 print("Page loaded but stock name not found (Structure might have changed or blocked).")
                 
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_detail_page()
