import requests

from auth.partners_api_auth import PartnersAuth
from basecase import BaseCase
from auth.enums import *

class TestUser(BaseCase):
    def setUp(self):
        super().setUp()
        self.auth_manager = PartnersAuth()
        self.url = f'{self.auth_manager.url}api/partners/user'
        self.mail = self.auth_manager.mail
        self.password = self.auth_manager.password
        self.auth_manager.get_token_user()
        self.auth_manager.get_token_back()

    def test_get_nps_user(self):
        body = {
            "email": self.mail,
            "firstName": "Test",
            "lastName": "Test",
            "sex": "F"}
        auth = self.auth_manager.authorization(BACK)
        response = requests.post(self.url, json=body, headers=auth)
        print(auth)
        self.assertEqual(response.json()['npsCid'], 'NP000541128')

    def test_user_addresses_list(self):
        body = {"npsCid": "NP000541128"}
        url = f'{self.url}/addresses'
        auth = self.auth_manager.authorization(BACK)
        response = requests.post(url, json=body, headers=auth)
        print(response.json())
        self.assertIsNotNone(response.json()['addresses'])
