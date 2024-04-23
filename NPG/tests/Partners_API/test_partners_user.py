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
        self.assertEqual(response.json().get('status'), 'ok', msg=response.json())
        self.assertEqual(response.json()['msg'], 'success')

        addr_response = self.user_addresses_request()['addresses']
        result = next((i for i in addr_response if i.get('id') == address_id), None)

        for key, value in updated_fields.items():
            self.assertEqual(value, result[key])

    def change_email(self, body=None):
        url = f'{self.url}/change-email'
        auth = self.auth_manager.authorization(BACK)
        if body is None:
            body = {
                "npsCid": "NP000541130",
                "email": "marsvolta@ukr.net",
                "newEmail": "marsvolta1@ukr.net"
            }
        response = requests.put(url, json=body, headers=auth)
        return response

    def test_get_nps_user(self):
        body = {
            "email": self.mail,
            "firstName": "Test",
            "lastName": "Test",
            "sex": "F",
            "phone": "+380500000000"}
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
                  'comment', 'isFavorite', 'branchRef', 'cityRef', 'settlementRef']
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
        self.update_and_check_address(413117, body)

    def test_update_user_address_department(self):
        body = {"branchRef": "1692286e-e1c2-11e3-8c4a-0050568002cf"}
        self.update_and_check_address(413115, body)

    def test_erase_fields(self):
        body = {"building": None,
                "comment": None}
        self.update_and_check_address(413117, body)

    def test_valid_change_email(self):
        body = {
            "npsCid": "NP000541130",
            "email": "marsvolta1@ukr.net",
            "newEmail": "marsvolta@ukr.net"
        }
        response = self.change_email()
        self.assertEqual('NP000541130', response.json().get('npsCid'), msg=response.json())

        response = self.change_email(body)
        self.assertEqual('NP000541130', response.json().get('npsCid'), msg=response.json())

    def test_invalid_change_email(self):
        body = {
            "npsCid": "NP000541130",
            "email": "marsvolta@ukr.net",
            "newEmail": "marsvolta@ukr.net"
        }
        response = self.change_email(body)
        self.assertEqual('Email already exists', response.json().get('errorDescription'))

        body['npsCid'] = 'NP000541131'
        response = self.change_email(body)
        self.assertEqual('This email does not belong to the user.', response.json().get('errorDescription'))

        body['email'] = 'marsvolta'
        response = self.change_email(body)
        self.assertEqual('Nothing processed', response.json().get('errorDescription'))

