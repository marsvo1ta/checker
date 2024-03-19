import requests

from auth.partners_api_auth import PartnersAuth
from basecase import BaseCase
from auth.enums import *


class TestUser(BaseCase):
    def setUp(self):
        super().setUp()
        self.auth_manager = PartnersAuth()
        self.url = f'{self.auth_manager.url}api/partners/shops'
        self.auth_manager.get_token_user()
        self.auth_manager.get_token_back()

    def params(self, country, search=None, page=None, size=None) -> dict:
        return {'country': country,
                'search': search,
                'page': page,
                'size': size}

    def get_shop_request(self, country, search=None, page=None, size=None):
        params = self.params(country, search, page, size)
        auth = self.auth_manager.authorization(BACK)
        response = requests.get(self.url, params=params, headers=auth)
        return response

    def test_shop_full_search(self):
        response = self.get_shop_request('US', 'Blue', 1, 10)

        self.assertIsNotNone(response.json()['items'])
        self.assertGreaterEqual(response.json()['page']['totalItems'], 1)

    def test_shop_country_search(self):
        response = self.get_shop_request('US', size=10)

        self.assertEqual(len(response.json()['items']), 10)
        self.assertGreaterEqual(response.json()['page']['totalItems'], 100)

    def test_shop_pagination(self):
        size = 10
        response = self.get_shop_request('US', size=size)

        total_items= response.json()['page']['totalItems']
        total_pages = response.json()['page']['totalPages']
        items_on_last_page = total_pages * size - total_items

        last_page_response = self.get_shop_request('US', size=size, page=total_pages)
        items_len = len(last_page_response.json()['items'])
        self.assertEqual(items_len, items_on_last_page)

    def test_shop_zero_items(self):
        response = self.get_shop_request('CN', search='Amazon')

        self.assertEqual(len(response.json()['items']), 0)
        self.assertEqual(response.json()['page']['totalItems'], 0)
        self.assertEqual(response.json()['page']['totalPages'], 0)

    def test_shop_nothing_processed(self):
        response = self.get_shop_request(None)

        self.assertEqual(response.json()['error'], 'invalid_entity')
        self.assertEqual(response.json()['errorDescription'], 'Nothing processed')
        self.assertEqual(response.json()['errors']['country'], 'value_required')
