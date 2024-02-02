import requests
from data.credentials import PARTNERS_PASS, PARTNERS_LOGIN, NPS_URL_STAGE, NPS_EURO_MAIL, NPS_PASS_PROD


class PartnersAuth:
    def __init__(self):
        self.mail = NPS_EURO_MAIL
        self.password = NPS_PASS_PROD
        self.basic_login = str(PARTNERS_LOGIN)
        self.basic_password = str(PARTNERS_PASS)
        self.url = NPS_URL_STAGE
        self.back_auth_url = f'{self.url}api/partners/login'
        self.user_auth_url = f'{self.url}api/user/login/password'
        self.back_token = {'Authorization': f'Bearer {self.get_token_back()}'}
        self.user_token = {'Authorization': f'Bearer {self.get_token_user()}'}

    def get_token_back(self):
        basic_auth = (self.basic_login, self.basic_password)
        body = {"login": "test_test",
                "password": "Password1"}

        response = requests.post(self.back_auth_url,
                                 auth=basic_auth,
                                 json=body)

        # try:
        return response.json()['token']
        # except:
        #     print(f'Виникла помилка. Відповідь: "{response.text}"')

    def get_token_user(self):
        body = {
            "email": self.mail,
            "password": self.password}

        response = requests.post(self.user_auth_url, json=body)
        # try:
        return response.json()['token']
        # except:
        #     print(f'Виникла помилка. Відповідь: "{response.text}"')


