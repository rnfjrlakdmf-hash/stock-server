
import sys
import os

# Add backend directory to path
sys.path.append(os.path.abspath("backend"))

from stock_data import get_market_news

print("Fetching market news...")
news = get_market_news()
print(f"Found {len(news)} news items.")
for n in news:
    print(f"- {n['title']} ({n['source']})")
