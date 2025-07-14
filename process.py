import re
from datetime import datetime, timedelta

def parse_posted_time(text):
    # e.g. text = "• 2 hours ago"
    match = re.search(r'(\d+)\s+(hour|day|month|minute)s?\s+ago', text)
    if not match:
        return None
    value = int(match.group(1))
    unit = match.group(2)
    if unit == 'minute':
        return datetime.now() - timedelta(minutes=value)
    elif unit == 'hour':
        return datetime.now() - timedelta(hours=value)
    elif unit == 'day':
        return datetime.now() - timedelta(days=value)
    elif unit == 'month':
        return datetime.now() - timedelta(days=30*value)
    return None

def extract_bounties_with_time(firecrawl_json):
    markdown = firecrawl_json["data"]["markdown"]
    lines = markdown.splitlines()

    bounties = []
    current_price = None
    current_posted_time = None

    for i, line in enumerate(lines):
        price_match = re.match(r'- \$([0-9,.]+)', line.strip())
        if price_match:
            current_price = float(price_match.group(1).replace(',', ''))
        
        # Check for posted time line (usually contains 'ago')
        if 'ago' in line:
            current_posted_time = parse_posted_time(line.strip())

        title_match = re.match(r'### \[(.*?)\]\((.*?)\)', line.strip())
        if title_match and current_price is not None:
            title = title_match.group(1)
            link = title_match.group(2)
            
            # Only keep bounty if posted within last 24 hours
            if current_posted_time and (datetime.now() - current_posted_time).total_seconds() <= 86400:
                bounties.append({
                    'title': title,
                    'link': link,
                    'price': current_price,
                    'posted_time': current_posted_time
                })
            current_price = None
            current_posted_time = None

    return bounties

def get_top_bounty(bounties):
    if not bounties:
        print("⚠️ No bounties found")
        return None
    top = max(bounties, key=lambda b: b['price'])
    print("🏆 Highest Bounty Found:")
    print(top)
    return top
