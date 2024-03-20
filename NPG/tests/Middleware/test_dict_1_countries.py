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
        self.url: str = f'{NPG_URL_PROD}countries'
        self.auth: dict = self.auth_manager.prod_admin_auth()

    def json_data(self, file_name: str):
        json_data = json_serialize(get_json_file_path(file_name, 'countries'))
        return json_data

    def metadata_params(self, limit=10, offset=0):
        params = {'limit': limit, 'offset': offset}
        return params

    def filters(self, field_name, value):
        params = {f'filter[{field_name}]': value}
        return params

    def get_list_request(self, params=None):
        return requests.get(self.url, params=params, headers=self.auth)

    def view_country_request(self, country_id):
        url = f'{self.url}/{country_id}'
        return requests.get(url, headers=self.auth)

    def test_get_countries(self):
        response = self.get_list_request()
        json_response = response.json()
        results_obj = json_response['results']
        metadata_obj = json_response['metadata']

        self.assertEqual(len(results_obj), 10)
        self.assertEqual(metadata_obj['limit'], 10)
        self.assertGreater(metadata_obj['total'], 200)

    def test_countries_pagination(self):
        params = self.metadata_params(1, 1)
        response = self.get_list_request(params)
        metadata_obj = response.json()['metadata']

        self.assertEqual(metadata_obj['limit'], 1)
        self.assertEqual(metadata_obj['offset'], 1)

        params = self.metadata_params(10, metadata_obj['total'] - 1)
        response = self.get_list_request(params)
        results_obj = response.json()['results']

        self.assertEqual(len(results_obj), 1)

        params = self.metadata_params(10, metadata_obj['total'])
        response = self.get_list_request(params)
        results_obj = response.json()['results']

        self.assertEqual(len(results_obj), 0)

    def test_countries_fields_validation(self):
        params = self.metadata_params(1, 1)
        response = self.get_list_request(params)
        result_item: dict = response.json()['results'][0]
        json_data: dict = self.json_data('list_response')
        json_flag_keys: dict = json_data['flag'].keys()
        result_flag_keys: dict = result_item['flag'].keys()
        json_pay_keys: dict = json_data['paymentSystem'].keys()
        result_pay_keys: dict = result_item['paymentSystem'].keys()

        # Delete this after deploy new fields to prod
        new_fields_placeholder = set(json_data.keys()) - set(result_item.keys())
        if new_fields_placeholder == {'zipCodeRequired', 'zipCodeExists'}:
            result_item.update({'zipCodeRequired': True, 'zipCodeExists': True})

        self.assertEqual(set(json_data.keys()), set(result_item.keys()))
        self.assertEqual(set(json_flag_keys), set(result_flag_keys))
        self.assertEqual(set(json_pay_keys), set(result_pay_keys))

    def test_countries_filters(self):
        filters = self.filters('code', 'FR')
        response = self.get_list_request(filters)
        results = response.json()['results'][0]

        self.assertEqual(results['code'], 'FR')

        filters = self.filters('name', 'France')
        response = self.get_list_request(filters)
        results = response.json()['results'][0]

        self.assertEqual(results['name'], 'France')

    def test_countries_multilang(self):
        self.auth.update({'Accept-Language': 'uk'})
        filters = self.filters('code', 'FR')
        response = self.get_list_request(filters)
        self.assertEqual(response.json()['results'][0]['name'], 'Франція')
        self.assertEqual(response.json()['results'][0]['currencyFullName'], 'Євро')

    def test_view_country(self):
        first_country_id = self.get_list_request().json()['results'][0]['id']
        response = self.view_country_request(first_country_id)

        response_data: dict = response.json()
        json_data: dict = self.json_data('view_response')

        # Delete this after deploy new fields to prod
        new_fields_placeholder = set(json_data.keys()) - set(response_data.keys())
        if new_fields_placeholder == {'eORIRequired', 'zipCodeExists', 'zipCodeRequired'}:
            response_data.update({'eORIRequired': True, 'zipCodeExists': True, 'zipCodeRequired': True})

        self.assertEqual(set(json_data.keys()), set(response_data.keys()))
        self.assertEqual(len(response_data['flag']), 5)
        self.assertEqual(len(response_data['name']), 3)
        self.assertEqual(len(response_data['cargoRequirement']), 3)
        self.assertEqual(len(response_data['currencyFullName']), 3)
        self.assertEqual(len(response_data['restrictionsDescription']), 3)
        self.assertEqual(len(response_data['paymentSystem']), 3)
