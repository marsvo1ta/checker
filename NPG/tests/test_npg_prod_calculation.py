import requests

from basecase import BaseCase
from data.credentials import NPG_URL_PROD
from auth.authorization import AuthManager
from json_data.json_serialize import json_serialize
from json_data.json_file_path import get_json_file_path


class TestCalculate(BaseCase):

    def setUp(self):
        super().setUp()
        self.auth_manager = AuthManager()
        self.url = f'{NPG_URL_PROD}international-express-waybills/calculate'
        self.auth = self.auth_manager.prod_admin_auth()

    def json_data(self, file_name: str):
        json_data = json_serialize(get_json_file_path(file_name))
        response = requests.post(self.url, headers=self.auth, json=json_data)
        return response

    def test_CA_UA(self):
        response = self.json_data('CA_UA_prod')
        self.assertEqual(response.status_code, 200)
        print()
        print(response.json()['deliveryPriceCost'])
        print(response.json()['domesticCurrencyCost'])

    def test_US_UA(self):
        response = self.json_data('US_UA_prod')
        self.assertEqual(response.status_code, 200)
        print()
        print(response.json()['deliveryPriceCost'])
        print(response.json()['domesticCurrencyCost'])

    def test_GB_UA(self):
        response = self.json_data('GB_UA_prod')
        self.assertEqual(response.status_code, 200)
        print()
        print(response.json()['deliveryPriceCost'])
        print(response.json()['domesticCurrencyCost'])

    def test_UA_PL_global(self):
        response = self.json_data('UA_PL_global_delivery_prod')
        self.assertEqual(response.status_code, 200)
        print()
        print(response.json()['deliveryPriceCost'])
        print(response.json()['domesticCurrencyCost'])

    def test_UA_PL_things(self):
        response = self.json_data('UA_PL_things_prod')
        self.assertEqual(response.status_code, 200)
        print()
        print(response.json()['deliveryPriceCost'])
        print(response.json()['domesticCurrencyCost'])
