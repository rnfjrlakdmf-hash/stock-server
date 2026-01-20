
from bs4 import BeautifulSoup
import re

print("Reading naver_dump.html...")
with open("naver_dump.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

print("--- Check IDs ---")
for selector in ["#_per", "#_pbr", "#_eps", "#_dvr", "#_cns_per", "#_cns_eps", "#_market_sum"]:
    tag = soup.select_one(selector)
    if tag:
        print(f"{selector}: '{tag.text.strip()}'")
    else:
        print(f"{selector}: Not Found")

print("\n--- Check Tables (TH) [ALL] ---")
for th in soup.select("th"):
    label = th.text.strip()
    td = th.find_next_sibling("td")
    val = td.text.strip() if td else "No TD"
    print(f"Header: '{label}' -> Value: '{val}'")

print("\n--- Check .no_info Table ---")
no_info = soup.select_one(".no_info")
if no_info:
    print("Found .no_info table")
    trs = no_info.select("tr")
    for i, tr in enumerate(trs):
        tds = tr.select("td")
        vals = [td.text.strip().replace('\n', '').replace('\t', '') for td in tds]
        print(f"Row {i}: {vals}")
else:
    print(".no_info table not found")
