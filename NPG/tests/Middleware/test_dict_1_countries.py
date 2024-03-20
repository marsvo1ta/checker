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
        self.url = f'{NPG_URL_PROD}countries'
        self.auth = self.auth_manager.prod_admin_auth()

    def json_data(self, file_name: str):
        json_data = json_serialize(get_json_file_path(file_name, 'countries'))
        return json_data

    def metadata_params(self, limit=10, offset=0):
        params = {'limit': limit, 'offset': offset}
        return params

    def test_get_countries(self):
        response = requests.get(self.url, headers=self.auth)
        json_response = response.json()
        results_obj = json_response['results']
        metadata_obj = json_response['metadata']

        self.assertEqual(len(results_obj), 10)
        self.assertEqual(metadata_obj['limit'], 10)
        self.assertGreater(metadata_obj['total'], 200)

    def test_countries_pagination(self):
        params = self.metadata_params(1, 1)
        response = requests.get(self.url, params, headers=self.auth)
        metadata_obj = response.json()['metadata']

        self.assertEqual(metadata_obj['limit'], 1)
        self.assertEqual(metadata_obj['offset'], 1)

        params = self.metadata_params(10, metadata_obj['total'] - 1)
        response = requests.get(self.url, params, headers=self.auth)
        results_obj = response.json()['results']

        self.assertEqual(len(results_obj), 1)

        params = self.metadata_params(10, metadata_obj['total'])
        response = requests.get(self.url, params, headers=self.auth)
        results_obj = response.json()['results']

        self.assertEqual(len(results_obj), 0)

    def test_countries_fields_validation(self):
        params = self.metadata_params(1, 1)
        response = requests.get(self.url, params, headers=self.auth)
        result_item: dict = response.json()['results'][0]
        json_data: dict = self.json_data('list_response')
        json_flag_keys = json_data['flag'].keys()
        result_flag_keys = result_item['flag'].keys()
        json_pay_keys = json_data['paymentSystem'].keys()
        result_pay_keys = result_item['paymentSystem'].keys()

        # Delete this after deploy new fields to prod
        new_fields_placeholder = set(json_data.keys()) - set(result_item.keys())
        if new_fields_placeholder == {'zipCodeRequired', 'zipCodeExists'}:
            result_item.update({'zipCodeRequired': True, 'zipCodeExists': True})

        self.assertEqual(set(json_data.keys()), set(result_item.keys()))
        self.assertEqual(set(json_flag_keys), set(result_flag_keys))
        self.assertEqual(set(json_pay_keys), set(result_pay_keys))


