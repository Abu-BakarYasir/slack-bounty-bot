from flask import Flask, request
from main import run_dynamic_bot
from main import run_dynamic_bot
import os

app = Flask(__name__)


@app.route('/run-bot')
def run_bot():
    # Verify CRON_SECRET
    auth_header = request.headers.get('Authorization')
    expected_secret = os.getenv('CRON_SECRET')
# Allow requests without auth_header if CRON_SECRET is unset or auth matches
    if expected_secret and auth_header and auth_header != f'Bearer {expected_secret}':
        return 'Unauthorized', 401
    try:
        run_dynamic_bot()
        return 'Bot executed successfully!', 200
    except Exception as e:
        return f'Error running bot: {str(e)}', 500

if __name__ == "__main__":
    app.run()