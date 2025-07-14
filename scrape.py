# scrape.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
TARGET_URL = "https://replit.com/bounties?status=open&order=creationDateDescending"
API_URL = "https://api.firecrawl.dev/v1/scrape"

def scrape_bounties_live():
    print("📡 Scraping Replit live...")
    if not FIRECRAWL_API_KEY:
        print("❌ ERROR: FIRECRAWL_API_KEY not found in .env")
        return None

    headers = {
        "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "url": TARGET_URL,
        "formats": ["markdown"]  # ✅ Proper Firecrawl API format
    }

    print("📦 Payload being sent to Firecrawl:", payload)

    try:
        res = requests.post(API_URL, json=payload, headers=headers)
        print(f"🌐 Firecrawl responded with status code: {res.status_code}")
        res.raise_for_status()
        print("✅ Live data fetched successfully")

        # # 💾 Optional: Save to file
        # with open("firecrawl_response.json", "w", encoding="utf-8") as f:
        #     import json
        #     json.dump(res.json(), f, ensure_ascii=False, indent=2)
        #     print("💾 Response saved to firecrawl_response.json")

        return res.json()

    except requests.exceptions.HTTPError:
        print("❌ HTTPError:", res.status_code, res.text)
        return None
    except requests.exceptions.RequestException as e:
        print("❌ RequestException:", str(e))
        return None
