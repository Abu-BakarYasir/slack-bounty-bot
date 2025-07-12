# scrape.py (modified)

import requests
import os
from dotenv import load_dotenv

load_dotenv()
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
TARGET_URL = "https://replit.com/bounties?status=open&order=creationDateDescending"
API_URL = "https://api.firecrawl.dev/v1/scrape"

def scrape_bounties_live():
    print("📡 Scraping Replit live...")
    headers = {
        "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = { "url": TARGET_URL }

    res = requests.post(API_URL, json=payload, headers=headers)
    res.raise_for_status()
    print("✅ Live data fetched")
    return res.json()
