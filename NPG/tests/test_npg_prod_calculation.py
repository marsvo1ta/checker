import os


import requests

from basecase import BaseCase
from data.credentials import NPG_URL_PROD, NPG_URL_STAGE
from auth.authorization import AuthManager
from json_data.json_serialize import json_serialize
from json_data.json_file_path import get_json_file_path


class TestCalculate(BaseCase):
    def setUp(self):
        super().setUp()
        self.auth_manager = AuthManager()

    def test_CA_UA(self):
        url = f'{NPG_URL_PROD}international-express-waybills/calculate'
        auth = self.auth_manager.prod_admin_auth()

        json_data = json_serialize(get_json_file_path('CA_UA_prod'))
        response = requests.post(url, headers=auth, json=json_data)

        self.assertEqual(response.status_code, 200)

        print(response.json()['deliveryPriceCost'])
        print(response.json()['domesticCurrencyCost'])

    def test_US_UA(self):
        url = f'{NPG_URL_PROD}international-express-waybills/calculate'
        auth = self.auth_manager.prod_admin_auth()

        json_data = json_serialize(get_json_file_path('US_UA_prod'))
        response = requests.post(url, headers=auth, json=json_data)

        self.assertEqual(response.status_code, 200)

        print(response.json()['deliveryPriceCost'])
        print(response.json()['domesticCurrencyCost'])