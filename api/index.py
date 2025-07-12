from flask import Flask
from main import run_dynamic_bot

app = Flask(__name__)

@app.route('/run-bot')
def run_bot():
    try:
        run_dynamic_bot()
        return 'Bot executed successfully!', 200
    except Exception as e:
        return f'Error running bot: {str(e)}', 500

if __name__ == "__main__":
    app.run()