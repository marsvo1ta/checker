import requests
from datetime import datetime
import pytz

from data.credentials import *


def get_current_time(timezone='Europe/Kiev', format='%d.%m.%Y %H:%M:%S'):
    tz = pytz.timezone(timezone)
    current_time = datetime.now(tz)
    formatted_time = current_time.strftime(format)
    return formatted_time


def send_telegram_message(bot_token, chat_id, message):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, json=payload)
    print(response.status_code)
    return response.json() if response.status_code == 200 else response.status_code


def send_telegram_sticker(bot_token, chat_id, sticker_id):

    url = f'https://api.telegram.org/bot{bot_token}/sendSticker'
    payload = {
        'chat_id': chat_id,
        'sticker': sticker_id
    }
    response = requests.post(url, json=payload)
    print(response.status_code)
    return response


with open('formatted_test_results.txt', 'r') as file:
    message = file.read()
bot_token = TELEGRAM_BOT_TOKEN
chat_id = TELEGRAM_CHAT_ID

if 'FAIL' in message.split():
    send_telegram_message(bot_token, chat_id, f'{get_current_time()}\n\n{message}')
    send_telegram_sticker(bot_token, chat_id, FAIL)
else:
    send_telegram_message(bot_token, chat_id, get_current_time())
    send_telegram_sticker(bot_token, chat_id, PASS)
