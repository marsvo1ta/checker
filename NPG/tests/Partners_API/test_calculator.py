import requests

from auth.partners_api_auth import PartnersAuth
from basecase import BaseCase
from auth.enums import *


class TestApiCalculator(BaseCase):
    def setUp(self):
        super().setUp()
        self.auth_manager = PartnersAuth()
        self.url = f'{self.auth_manager.url}api/public/calculator/accounting'
        self.header = {'Accept': 'application/json',
                       'Authorization': 'Basic bnBpOiE5TXQzRXV5Y1I1NQ==',
                       'Locale': 'en'}

    def calculator_json(self):
        body = {
            "country": "US",
            "weight": 1.5,
            "cost": 10,
            "unit": "kg",
            "currency": "USD"
        }
        return body

    def test_us(self):
        body = self.calculator_json()
        response = requests.post(self.url, json=body, headers=self.header)
        self.assertEqual(200, response.status_code, msg=self.url)
        self.assertEqual(0, response.json().get('customPrice'))
        self.assertEqual(15, response.json().get('servicePrice'))
        self.assertEqual('USD', response.json().get('currency'))
        self.assertEqual(True, response.json().get('status'))
        self.assertGreater(response.json().get('totalPriceUah'), 590)

    def test_us_with_customs(self):
        body = self.calculator_json()
        body['cost'] = 200
        response = requests.post(self.url, json=body, headers=self.header)
        self.assertGreater(response.json().get('customPrice'), 15)
        self.assertGreater(response.json().get('totalPriceUah'), 1500)

    def test_eu(self):
        body = self.calculator_json()
        body['country'] = 'FR'
        body['currency'] = 'EUR'
        response = requests.post(self.url, json=body, headers=self.header)
        self.assertEqual(200, response.status_code, msg=self.url)
        self.assertEqual(0, response.json().get('customPrice'))
        self.assertEqual('EUR', response.json().get('currency'))
        self.assertEqual(True, response.json().get('status'))
        self.assertGreater(response.json().get('totalPriceUah'), 300)

    def test_eu_with_customs(self):
        body = self.calculator_json()
        body['cost'] = 151
        body['country'] = 'FR'
        body['currency'] = 'EUR'
        response = requests.post(self.url, json=body, headers=self.header)
        self.assertGreater(response.json().get('customPrice'), 0)
        self.assertGreater(response.json().get('totalPriceUah'), 300)

    def test_greater_weight(self):
        body = self.calculator_json()
        body['weight'] = 201
        response = requests.post(self.url, json=body, headers=self.header)
        self.assertEqual('This value should be between 0 and 200.', response.json().get('errors').get('weight'))

        body['country'] = 'PL'
        body['currency'] = 'EUR'
        response = requests.post(self.url, json=body, headers=self.header)
        self.assertEqual('This value should be between 0 and 200.', response.json().get('errors').get('weight'))