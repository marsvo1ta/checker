
import requests
from data.credentials import *


class AuthManager:
    def __init__(self):
        self.token = None
        self.token_file = "token.txt"

    def stage_admin_auth(self):
        return {'Authorization': f'Bearer {self.get_token("stage")}'}

    def prod_admin_auth(self):
        return {'Authorization': f'Bearer {self.get_token("prod")}'}

    def get_token(self, environment):
        if self.token is None or not self.is_token_valid(self.token):
            self.token = self.load_token_from_file(environment)
            if self.token is None or not self.is_token_valid(self.token):
                self.token = self.fetch_and_save_token(environment)
        return self.token

    def is_token_valid(self, token):
        auth_headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(f'{NPG_URL_PROD}manufacturing-materials', headers=auth_headers)
        return response.status_code == 200

    def load_token_from_file(self, environment):
        if os.path.exists(self.token_file):
            with open(self.token_file, "r") as file:
                return file.read().strip()
        return None

    def fetch_and_save_token(self, environment):
        token = self.login(environment)
        if token:
            with open(self.token_file, "w") as file:
                file.write(token)
        return token

    def login(self, environment):
        body = {
            'email': NPG_ADMIN_EMAIL,
            'password': NPG_ADMIN_PASS
        }
        url = f'{NPG_URL_STAGE if environment == "stage" else NPG_URL_PROD}login/admin'
        response = requests.post(url, json=body)
        if response.status_code == 200:
            return response.json()['token']
        return None
