
import requests
import json
import urllib.parse

def search_naver_stock(query):
    try:
        encoded_query = urllib.parse.quote(query.encode('euc-kr'))
        url = f"https://ac.finance.naver.com/ac?q={encoded_query}&q_enc=euc-kr&st=111&r_format=json&r_enc=euc-kr"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://finance.naver.com/"
        }
        res = requests.get(url, headers=headers)
        data = res.json()
        
        # Structure: {'items': [[['Name', 'Code', ...], ...]]}
        if 'items' in data and len(data['items']) > 0:
            for item in data['items'][0]:
                print(f"Found: {item[0]} -> {item[1]}")
                return item[1] # Return first Code
    except Exception as e:
        print(f"Error: {e}")
        return None

search_naver_stock("카카오")
search_naver_stock("삼성전자")
