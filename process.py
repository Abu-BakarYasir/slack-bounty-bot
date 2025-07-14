import re
from datetime import datetime, timedelta

def parse_posted_time(text):
    # Matches: "2 hours ago", "1 day ago", etc.
    match = re.search(r'(\d+)\s+(minute|hour|day|month)s?\s+ago', text)
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
        return datetime.now() - timedelta(days=30 * value)
    return None

def extract_bounties_with_time(firecrawl_json):
    markdown = firecrawl_json["data"]["markdown"]
    lines = markdown.splitlines()

    bounties = []
    current_price = None
    current_posted_time = None
    current_title = None
    current_link = None
    description_lines = []
    user = None
    due_date = None

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Parse price
        price_match = re.match(r'- \$([0-9,.]+)', line)
        if price_match:
            current_price = float(price_match.group(1).replace(',', ''))

        # Parse posted time
        if 'ago' in line:
            current_posted_time = parse_posted_time(line)

        # Parse title and link
        title_match = re.match(r'### \[(.*?)\]\((.*?)\)', line)
        if title_match:
            current_title = title_match.group(1)
            current_link = title_match.group(2)

            # Look ahead for description, due date, and user
            description_lines = []
            user = None
            due_date = None

            for j in range(i+1, min(i+15, len(lines))):
                lookahead = lines[j].strip()

                # Stop parsing if a new bounty starts
                if lookahead.startswith("### ["):
                    break

                # Parse due date
                if 'due' in lookahead:
                    due_match = re.search(r'due\s+(.*?)(?:\n|$)', lookahead)
                    if due_match:
                        due_date = due_match.group(1).strip()

                # Parse bounty poster
                if re.match(r'\[.*\]\(https://replit\.com/@.*\)', lookahead):
                    user_match = re.match(r'\[(.*?)\]\(.*?\)', lookahead)
                    if user_match:
                        user = user_match.group(1)

                description_lines.append(lookahead)

            description = ' '.join(description_lines).strip()

            # Filter only recent bounties (within 24 hours)
            if current_posted_time and (datetime.now() - current_posted_time).total_seconds() <= 86400:
                bounties.append({
                    'title': current_title,
                    'link': current_link,
                    'price': current_price,
                    'posted_time': current_posted_time,
                    'description': description
                })

            # Reset after each bounty
            current_price = None
            current_posted_time = None
            current_title = None
            current_link = None

        i += 1

    return bounties

def get_top_bounties(bounties):
    if not bounties:
        print("⚠️ No bounties found")
        return []

    max_price = max(b['price'] for b in bounties)
    top_bounties = [b for b in bounties if b['price'] == max_price]

    print(f"🏆 Found {len(top_bounties)} top bounties at ${max_price}:")
    for b in top_bounties:
        print(b)

    return top_bounties
