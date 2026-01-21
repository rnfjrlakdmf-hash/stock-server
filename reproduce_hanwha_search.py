
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import quote

def search_korean_stock_symbol_debug(keyword: str):
    print(f"Searching for: {keyword}")
    try:
        # euc-kr Encoding for Naver Query
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
            
        print(f"HTML length: {len(html)}")
            
        soup = BeautifulSoup(html, 'html.parser')
        
        # Check for direct match table
        # .tbl_search result
        results = soup.select(".tbl_search tbody tr")
        print(f"Found {len(results)} rows in table")
        
        for i, row in enumerate(results):
            cols = row.select("td")
            if len(cols) >= 1:
                title_link = cols[0].select_one("a")
                print(f"Row {i} col 0 text: {title_link.text if title_link else 'No Link'}")
                if title_link:
                    name = title_link.text.strip()
                    # href="/item/main.naver?code=005930"
                    href = title_link['href']
                    print(f"  Href: {href}")
                    code_match = re.search(r'code=(\d+)', href)
                    if code_match:
                        code = code_match.group(1)
                        if name == keyword: # Exact match check?
                            print(f"  Exact match code: {code}")
                        else:
                            print(f"  Partial/Other match code: {code}")
                        
                        # logic in actual code returns first match immediately
                        return code
                        
        print("No match found in rows")
        return None
        
    except Exception as e:
        print(f"Search Symbol Error: {e}")
        return None

if __name__ == "__main__":
    result = search_korean_stock_symbol_debug("한화오션")
    print(f"Result: {result}")
