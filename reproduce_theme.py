import sys
import os
import json
import logging

# Configure logging to show everything
logging.basicConfig(level=logging.DEBUG)

# Add backend to sys.path
# Assuming running from root (c:\Users\rnfjr\StockTrendProgram)
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from ai_analysis import analyze_theme

def test_theme():
    print("Analyzing theme '우주항공'...")
    try:
        result = analyze_theme("우주항공")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        followers = result.get('followers', [])
        print(f"\nFollowers count: {len(followers)}")
        if not followers:
            print("Followers list is empty!")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_theme()
