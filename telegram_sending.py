import requests
from datetime import datetime
import pytz

from data.credentials import *

bot_token = TELEGRAM_BOT_TOKEN
chat_id = TELEGRAM_CHAT_ID


def add_tag(tag, text):
    return f'<{tag}>{text}</{tag}>'


def bold(text):
    return add_tag('b', text)


def get_current_time(timezone='Europe/Kiev', format='%d.%m.%Y %H:%M:%S'):
    tz = pytz.timezone(timezone)
    current_time = datetime.now(tz)
    formatted_time = current_time.strftime(format)
    return f'<b>{formatted_time}</b>'


def send_telegram_message(bot_token, chat_id, message, parse_mode='None'):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': parse_mode
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


if 'FAIL' in message.split():
    send_telegram_message(bot_token, chat_id, f'{get_current_time()}\n\n{message}', 'HTML')
    send_telegram_sticker(bot_token, chat_id, FAIL)
else:
    send_telegram_message(bot_token, chat_id, f'{get_current_time()}\n\n{bold("Усі тести пройшли успішно")}', 'HTML')
    send_telegram_sticker(bot_token, chat_id, PASS)
