import requests

from basecase import BaseCase
from data.credentials import NPG_URL_PROD
from auth.authorization import AuthManager
from json_data.json_serialize import json_serialize
from json_data.json_file_path import get_json_file_path


class TestCalculate(BaseCase):

    def setUp(self):
        super().setUp()
        self.url = 'https://npg-ddc-backend-prod.c1.npshopping.com/v1.0/search/cargo?country-code=ua&locale=uk'

    def test_ddc(self):
        keywords_list = ['куртка', 'шорти', 'мʼяч', 'штани']
        for idx, word in enumerate(keywords_list):
            response = requests.get(f'{self.url}{word}')
            print(response.json())
            self.assertIsNotNone(response.json()['items'])

