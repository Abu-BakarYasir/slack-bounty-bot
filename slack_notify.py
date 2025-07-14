# slack_notify.py

import json
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

if not SLACK_WEBHOOK_URL:
    raise ValueError("Slack webhook missing in .env")


def send_to_slack(bounty):
    if not SLACK_WEBHOOK_URL:
        raise ValueError("Slack webhook missing in .env")

    # ⏱️ Calculate how long ago it was posted
    if bounty.get('posted_time'):
        delta = datetime.now() - bounty['posted_time']
        seconds = delta.total_seconds()
        if seconds < 60:
            posted = "just now"
        elif seconds < 3600:
            posted = f"{int(seconds // 60)} minutes ago"
        elif seconds < 86400:
            posted = f"{int(seconds // 3600)} hours ago"
        else:
            posted = f"{int(seconds // 86400)} days ago"
    else:
        posted = "Unknown"

    # 📄 Clean up long description
    description = bounty.get("description", "").strip()
    if len(description) > 500:
        description = description[:500].rstrip() + "..."

    payload = {
        "text": (
            f"*New High-Value Bounty Alert!*\n\n"
            f"*Title:* {bounty['title']}\n"
            f"*Price:* ${bounty['price']}\n"
            f"*Posted:* {posted}\n"
            f"*Description:*\n```{description}```\n"
            f"🔗 <{bounty['link']}|View Full Bounty on Replit>"
        )
    }

    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    if response.status_code == 200:
        print("✅ Slack message sent!")
    else:
        print(f"❌ Slack Error: {response.status_code}")
        print(response.text)
