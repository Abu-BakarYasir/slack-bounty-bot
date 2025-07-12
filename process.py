# process.py (modified)

import re


def extract_bounties_from_data(firecrawl_json):
    try:
        markdown = firecrawl_json["data"]["markdown"]
        print("🧾 Markdown Preview:\n", markdown[:500])
    except KeyError:
        print("❌ No markdown in FireCrawl response.")
        return []

    lines = markdown.splitlines()
    bounties = []
    current_price = None

    for line in lines:
        price_match = re.match(r'- \$([0-9,.]+)', line.strip())
        if price_match:
            current_price = float(price_match.group(1).replace(',', ''))

        title_match = re.match(r'### \[(.*?)\]\((.*?)\)', line.strip())
        if title_match and current_price is not None:
            title = title_match.group(1)
            link = title_match.group(2)

            bounties.append({
                'title': title,
                'link': link,
                'price': current_price
            })
            current_price = None

    return bounties

def get_top_bounty(bounties):
    if not bounties:
        print("⚠️ No bounties found")
        return None
    top = max(bounties, key=lambda b: b['price'])
    print("🏆 Highest Bounty Found:")
    print(top)
    return top
