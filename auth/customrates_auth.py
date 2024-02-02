
import requests
from data.credentials import *


class CustomRatesAuthManager:
    def __init__(self, auth_url, client_id, client_secret):
        self.auth_url = auth_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None
        self.key = CUSTOMRATES_KEY_STAGE

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
