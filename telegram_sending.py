import requests
from data.credentials import *


def send_telegram_message(bot_token, chat_id, message):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, json=payload)
    return response.json()


with open('formatted_test_results.txt', 'r') as file:
    message = file.read()
bot_token = TELEGRAM_BOT_TOKEN
chat_id = TELEGRAM_CHAT_ID

send_telegram_message(bot_token, chat_id, message)
