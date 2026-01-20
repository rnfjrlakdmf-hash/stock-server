
import requests
import sys

def debug_fetch(symbol):
    code = symbol.split('.')[0]
    url = f"https://finance.naver.com/item/main.naver?code={code}"
    headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" }
    
    print(f"Fetching {url}...")
    res = requests.get(url, headers=headers)
    
    print(f"Status: {res.status_code}")
    print(f"Encoding (requests detected): {res.encoding}")
    print(f"Apparent Encoding: {res.apparent_encoding}")
    print(f"Content-Type: {res.headers.get('Content-Type')}")
    
    content = res.content
    print(f"First 100 bytes (hex): {content[:100].hex()}")
    
    # Try Explicit CP949
    try:
        decoded_cp949 = content.decode('cp949')
        print("Success decoding CP949")
        # Find title
        if "<title>" in decoded_cp949:
             start = decoded_cp949.find("<title>")
             end = decoded_cp949.find("</title>")
             print(f"Title (CP949): {decoded_cp949[start:end+8]}")
    except Exception as e:
        print(f"Failed decoding CP949: {e}")

    # Try Explicit EUC-KR
    try:
        decoded_euc = content.decode('euc-kr')
        print("Success decoding EUC-KR")
    except Exception as e:
        print(f"Failed decoding EUC-KR: {e}")
        
    # Try Explicit UTF-8
    try:
        decoded_utf8 = content.decode('utf-8')
        print("Success decoding UTF-8")
        if "<title>" in decoded_utf8:
             start = decoded_utf8.find("<title>")
             end = decoded_utf8.find("</title>")
             print(f"Title (UTF-8): {decoded_utf8[start:end+8]}")
    except Exception as e:
        print(f"Failed decoding UTF-8: {e}")


if __name__ == "__main__":
    debug_fetch("005930")
