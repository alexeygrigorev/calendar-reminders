import os
import requests

def send_telegram_message(message):
    """Send a message to a Telegram chat specified by TELEGRAM_CHAT_ID."""
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    send_text = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={message}'

    response = requests.get(send_text)
    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print(f"Failed to send message: {response.text}")
