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

    def assertions(self, response):
        body = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertGreater(body['deliveryPriceCost']['amount'], 0)

    def working_routes(self, response):
        body = response.json()
        all_routes = body['services']
        return [i for i in all_routes if '_1' in i]

    def logs(self, response):
        body = response.json()
        print(f"\n{body['deliveryPriceCost']}\n"
              f"{body['domesticCurrencyCost']}\n"
              f"{self.working_routes(response)}")
        print(body['services'][-1])

    def test_CA_UA(self):
        response = self.json_data('CA_UA_prod')
        self.assertions(response)
        self.logs(response)

    def test_US_UA(self):
        response = self.json_data('US_UA_prod')
        self.assertions(response)
        self.logs(response)

    def test_GB_UA(self):
        response = self.json_data('GB_UA_prod')
        self.assertions(response)
        self.logs(response)

    def test_UA_PL_global(self):
        response = self.json_data('UA_PL_global_delivery_prod')
        self.assertions(response)
        self.logs(response)

    def test_UA_PL_things(self):
        response = self.json_data('UA_PL_things_prod')
        self.assertions(response)
        self.logs(response)
