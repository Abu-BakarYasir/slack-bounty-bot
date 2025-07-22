# 🚀 Replit Bounty Notifier

This Python microservice dynamically scrapes **open bounties** from [Replit Bounties](https://replit.com/bounties), filters the **most valuable** ones posted in the last 24 hours, and sends a **Slack notification** to your channel.

✅ Deployed as a Flask API on **Vercel**, so you can trigger it from CRON jobs or external services.

---

### 📦 Project Structure

```

.
├── main.py                # Dynamic bot flow (scrape → filter → notify)
├── scrape.py              # Firecrawl API integration
├── slack\_notify.py        # Send messages to Slack
├── process.py             # Parse and filter bounty data
├── app.py                 # Flask app with /run-bot endpoint
├── .env                   # Secrets (ignored)
├── .gitignore
└── README.md

````

---

### ⚙️ Setup

#### 1️⃣ Clone & install dependencies

```bash
git clone https://github.com/yourusername/replit-bounty-notifier.git
cd replit-bounty-notifier
pip install -r requirements.txt
````

#### 2️⃣ Create `.env` file

```ini
FIRECRAWL_API_KEY=your_firecrawl_api_key
SLACK_WEBHOOK_URL=your_slack_webhook_url
CRON_SECRET=your_secret_token  # optional, for securing the /run-bot endpoint
```

---

### 🧪 Run locally

```bash
python app.py
```

Then visit:

```
http://127.0.0.1:5000/run-bot
```

> If you set `CRON_SECRET`, include in header:
>
> ```
> Authorization: Bearer your_secret_token
> ```

---

### 🌐 Deploy to Vercel

1. Push your project to GitHub
2. Connect the repo on [Vercel](https://vercel.com)
3. Add environment variables in Vercel dashboard:

   * `FIRECRAWL_API_KEY`
   * `SLACK_WEBHOOK_URL`
   * `CRON_SECRET` (optional)
4. Deploy 🚀

After deployment, your bot will run when you visit:

```
https://your-vercel-project.vercel.app/run-bot
```

---

### 📜 How it works

* `scrape.py`: Fetches live bounties from Firecrawl API as Markdown
* `process.py`: Parses title, price, posted time, description, etc.
* Filters bounties posted within last 24 hours
* Finds the highest priced bounty
* `slack_notify.py`: Formats and sends message to Slack

---

### ✏️ Example Slack Message

> *New High-Value Bounty Alert!*
>
> **Title:** Build a ChatGPT plugin
> **Price:** \$1500
> **Posted:** just now
> **Description:** Short description here...
>
> 🔗 [View Full Bounty on Replit](https://replit.com/bounties/...)

<img width="923" height="692" alt="image" src="https://github.com/user-attachments/assets/3a7ee29c-d34d-4799-9779-3f0ed2697e27" />

---

### 🛡 Security

* Secrets like API keys and Slack webhook are stored in `.env` (included in `.gitignore`)
* `/run-bot` endpoint can be protected with `CRON_SECRET` token

---

### 🛠 Built With

* Python + Flask
* Firecrawl API
* Slack Incoming Webhooks
* Vercel (serverless deployment)

---
