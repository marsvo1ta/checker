import requests

from auth.partners_api_auth import PartnersAuth
from basecase import BaseCase


class TestUser(BaseCase):
    def setUp(self):
        super().setUp()
        self.auth_manager = PartnersAuth()
        self.url = f'{self.auth_manager.url}api/partners/user'
        self.mail = self.auth_manager.mail
        self.password = self.auth_manager.password
        self.auth_back = self.auth_manager.back_token
        self.auth_user = self.auth_manager.user_token

    def test_get_nps_user(self):
        body = {
            "email": self.mail,
            "firstName": "Test",
            "lastName": "Test",
            "sex": "F"}
        response = requests.post(self.url, json=body, headers=self.auth_back)
        self.assertEqual(response.json()['npsCid'], 'NP000541128')

    def test_user_addresses_list(self):
        body = {"npsCid": "NP000541128"}
        url = f'{self.url}/addresses'
        response = requests.post(url, json=body, headers=self.auth_back)
        self.assertIsNotNone(response.json()['addresses'])
