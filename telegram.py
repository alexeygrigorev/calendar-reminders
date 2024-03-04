import os
import requests


BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')


def send_telegram_message(message):
    """Send a message to a Telegram chat specified by TELEGRAM_CHAT_ID."""

    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print(f"Failed to send message: {response.text}")
