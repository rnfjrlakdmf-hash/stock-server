
import requests
from urllib.parse import quote
from bs4 import BeautifulSoup

def inspect_html():
    keyword = "한화오션"
    encoded_query = quote(keyword.encode('euc-kr'))
    url = f"https://finance.naver.com/search/searchList.naver?query={encoded_query}"
    
    print(f"URL: {url}")
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    res = requests.get(url, headers=headers)
    
    # Decode
    try:
        html = res.content.decode('euc-kr')
    except:
        html = res.text
        
    soup = BeautifulSoup(html, 'html.parser')
    
    # Check for direct match table
    # .tbl_search result
    results = soup.select(".tbl_search tbody tr")
    print(f"Found {len(results)} rows.")
    
    for i, row in enumerate(results):
        print(f"Row {i}: {row.get_text(strip=True)}")
        cols = row.select("td")
        if len(cols) >= 1:
            title_link = cols[0].select_one("a")
            if title_link:
                print(f"  Link: {title_link['href']}, Text: {title_link.text}")

if __name__ == "__main__":
    inspect_html()
