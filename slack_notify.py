# slack_notify.py

import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_to_slack(bounty):
    if not SLACK_WEBHOOK_URL:
        raise ValueError("Slack webhook missing in .env")

    payload = {
        "text": f"*New High-Value Bounty!*\n"
                f"*Title:* {bounty['title']}\n"
                f"*Price:* ${bounty['price']}\n"
                f"<{bounty['link']}|View Bounty>"
    }

    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    if response.status_code == 200:
        print("✅ Slack message sent!")
    else:
        print(f"❌ Slack Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    from process import extract_bounties, get_top_bounty
    bounties = extract_bounties()
    top = get_top_bounty(bounties)
    if top:
        send_to_slack(top)
