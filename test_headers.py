
import requests
from urllib.parse import quote
from bs4 import BeautifulSoup

def test_headers():
    keyword = "한화오션"
    encoded_query = quote(keyword.encode('euc-kr'))
    url = f"https://finance.naver.com/search/searchList.naver?query={encoded_query}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://finance.naver.com/",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,ko;q=0.8",
        "Connection": "keep-alive"
    }
    
    print(f"Testing URL: {url} with headers")
    try:
        res = requests.get(url, headers=headers, timeout=10)
        print(f"Status Code: {res.status_code}")
        
        # Decode
        try:
            html = res.content.decode('euc-kr')
        except:
            html = res.text
            
        soup = BeautifulSoup(html, 'html.parser')
        
        # Check for error
        if soup.select(".error_content"):
            print("Still blocked (Error content found)")
        else:
            print("Success? (No error content)")
            results = soup.select(".tbl_search tbody tr")
            print(f"Found {len(results)} rows.")
            for row in results:
                print(row.get_text(strip=True))
                
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_headers()
