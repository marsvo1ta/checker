import os

import pytest
import requests

from basecase import BaseCase
from data.credentials import NPG_URL_PROD, NPG_URL_STAGE
from auth.authorization import AuthManager
from json_data.json_serialize import json_serialize


class TestCalculate(BaseCase):
    def setUp(self):
        super().setUp()
        self.auth_manager = AuthManager()

    def test_CA_UA(self):
        url = f'{NPG_URL_PROD}international-express-waybills/calculate'
        auth = self.auth_manager.prod_admin_auth()

        json_file_path = '/Users/anton/Documents/health_checker/json_data/calculate/CA_UA_prod.json'
        json_data = json_serialize(json_file_path)

        response = requests.post(url, headers=auth, json=json_data)
        self.assertEqual(response.status_code, 200)
        print(response.json()['deliveryPriceCost'])
        print(response.json()['domesticCurrencyCost'])
