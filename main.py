# main.py (dynamic flow)

from scrape import scrape_bounties_live
from process import extract_bounties_from_data, get_top_bounty
from slack_notify import send_to_slack

def run_dynamic_bot():
    print("🚀 Running dynamic bounty bot")

    live_data = scrape_bounties_live()
    bounties = extract_bounties_from_data(live_data)
    if not bounties:
        print("⚠️ No bounties found, aborting.")
        return

    top = get_top_bounty(bounties)
    if top:
        send_to_slack(top)

if __name__ == "__main__":
    run_dynamic_bot()
