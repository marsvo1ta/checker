
import requests
from data.credentials import *


class CustomRatesAuthManager:
    def __init__(self, env):
        self.url = None
        self.auth_url = None
        self.client_id = None
        self.client_secret = None
        self.token = None
        self.key = None
        self.environment(env)

    def environment(self, env='stage'):
        if env == 'stage':
            self.url = CUSTOMRATES_STAGE
            self.auth_url = CUSTOMRATES_AUTH_STAGE
            self.client_id = CUSTOMRATES_CLIENT_ID_STAGE
            self.client_secret = CUSTOMRATES_CLIENT_SECRET_STAGE
            self.key = CUSTOMRATES_KEY_STAGE
        else:
            self.url = CUSTOMRATES_PROD
            self.auth_url = CUSTOMRATES_AUTH_PROD
            self.client_id = CUSTOMRATES_CLIENT_ID_PROD
            self.client_secret = CUSTOMRATES_CLIENT_SECRET_PROD
            self.key = CUSTOMRATES_KEY_PROD

    def get_token(self):
        response = requests.post(
            self.auth_url,
            data={
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'grant_type': 'client_credentials',
            }
        )

        if response.status_code == 200:
            self.token = response.json().get('access_token')
            print("Токен отримано успішно.")
        else:
            print(f"Не вдалося отримати токен. Код помилки: {response.status_code}")
            self.token = None

    def auth(self):
        self.get_token()
        auth_dict = {'Authorization': self.token, 'x-api-key': self.key}
        return auth_dict
