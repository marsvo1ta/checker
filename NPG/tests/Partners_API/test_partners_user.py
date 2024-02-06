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

    def user_addresses_request(self):
        body = {"npsCid": "NP000541128"}
        url = f'{self.url}/addresses'
        auth = self.auth_manager.authorization(BACK)
        response = requests.post(url, json=body, headers=auth)
        return response.json()

    def update_and_check_address(self, address_id, updated_fields):
        url = f'{self.url}/addresses/update'
        auth = self.auth_manager.authorization(BACK)

        body = {"npsCid": "NP000541128", "addressId": address_id}
        body.update(updated_fields)

        response = requests.post(url, json=body, headers=auth)
        self.assertEqual(response.json()['status'], 'ok')
        self.assertEqual(response.json()['msg'], 'success')

        addr_response = self.user_addresses_request()['addresses']
        result = next((i for i in addr_response if i.get('id') == address_id), None)

        for key, value in updated_fields.items():
            self.assertEqual(value, result[key])

    def test_get_nps_user(self):
        body = {
            "email": self.mail,
            "firstName": "Test",
            "lastName": "Test",
            "sex": "F"}
        auth = self.auth_manager.authorization(BACK)
        response = requests.post(self.url, json=body, headers=auth)
        self.assertEqual(response.json()['npsCid'], 'NP000541128')

    def test_user_addresses_list(self):
        response = self.user_addresses_request()
        address = response['addresses']
        self.assertIsNotNone(address)
        for i in address:
            self.assertIsNotNone(i['type'])

    def test_user_addresses_fields(self):
        response = self.user_addresses_request()['addresses'][0]
        fields = ['id', 'country', 'type', 'city', 'street',
                  'house', 'building', 'flat', 'zipcode',
                  'comment', 'isFavorite', 'branchRef']
        for i in response:
            self.assertIn(i, fields)

    def test_update_user_address_door(self):
        body = {
            "country": "UA",
            "city": "Одеса",
            "branchRef": None,
            "street": "Італійський бульвар",
            "house": "4",
            "building": "1",
            "flat": "19",
            "zipcode": "65012",
            "comment": None,
            "isFavorite": True
        }
        self.update_and_check_address(412863, body)

    def test_update_user_address_department(self):
        body = {"branchRef": "511fd00e-e1c2-11e3-8c4a-0050568002cf"}
        self.update_and_check_address(412857, body)

    def test_erase_fields(self):
        body = {"building": None,
                "comment": None}
        self.update_and_check_address(412863, body)