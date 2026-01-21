
import requests
from urllib.parse import quote

def dump_html():
    keyword = "한화오션"
    encoded_query = quote(keyword.encode('euc-kr'))
    url = f"https://finance.naver.com/search/searchList.naver?query={encoded_query}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    res = requests.get(url, headers=headers)
    
    # Decode
    try:
        html = res.content.decode('euc-kr')
    except:
        html = res.text
        
    with open("naver_search_dump.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Dumped to naver_search_dump.html")

if __name__ == "__main__":
    dump_html()
