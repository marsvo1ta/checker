from data.credentials import *
import requests


def send_telegram_message():
    bot_token = TELEGRAM_BOT_TOKEN
    chat_id = TELEGRAM_BOT_TOKEN
    with open('formatted_test_results.txt', 'r') as file:
        message = file.read()
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, json=payload)
    return response.json()


send_telegram_message()
