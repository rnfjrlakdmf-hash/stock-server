
import requests
from bs4 import BeautifulSoup

def get_naver_flash_news():
    """네이버 금융 주요뉴스 크롤링 (Fallback)"""
    url = "https://finance.naver.com/news/mainnews.naver"
    headers = { "User-Agent": "Mozilla/5.0" }
    news_list = []
    
    try:
        res = requests.get(url, headers=headers)
        # cp949 decoding for Naver Finance
        soup = BeautifulSoup(res.content.decode('cp949', 'ignore'), 'html.parser')
        
        # Select news items
        # Structure often: ul.newsList or similar. Let's inspect typical structure via broad search
        # Actually mainnews uses .mainNewsList in some versions, or ul class="newsList"
        
        # Let's try select generic logic
        
        # Inspecting standard Naver Finance News structure
        articles = soup.select(".mainNewsList li")
        
        if not articles:
            print("No articles found with .mainNewsList li")
            # Try another selector
            articles = soup.select("ul.realtimeNewsList li")
            
        for li in articles:
            dt_a = li.select_one("dl dt a") # sometimes subject is in dt
            dd_a = li.select_one("dl dd.articleSubject a") # sometimes in dd
            
            target = dd_a if dd_a else dt_a
            
            if not target: continue
            
            title = target.text.strip()
            link = "https://finance.naver.com" + target['href']
            
            summ = li.select_one("dd.articleSummary")
            source = "Naver Finance"
            if summ:
                press = summ.select_one(".press")
                if press: source = press.text.strip()
                
            news_list.append({
                "source": source,
                "title": title,
                "link": link,
                "time": "최신"
            })
            
    except Exception as e:
        print(f"Naver News Fallback Error: {e}")
        
    return news_list

news = get_naver_flash_news()
print(f"Found {len(news)} items")
for n in news:
    print(n)
