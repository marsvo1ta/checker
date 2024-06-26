import requests

from basecase import BaseCase
from data.credentials import NPG_DDC_PROD, NPG_DDC_STAGE
from data.country_codes.country_codes import *


class TestLocalities(BaseCase):

    def setUp(self):
        super().setUp()
        self.url = f'{NPG_DDC_PROD}search/localities'
        # self.url = f'{NPG_DDC_STAGE}search/localities'

        self.codes = CODES
        self.keywords_en = KEYWORDS_EN
        self.keywords_ua = KEYWORDS_UA
        self.cities_en = CITIES_EN
        self.cities_ua = CITIES_UA

        self.en_dict = dict(zip(self.codes, self.keywords_en))
        self.ua_dict = dict(zip(self.codes, self.keywords_ua))

    @staticmethod
    def parameters(country_code, keyword: str, size, locale=''):
        params = {'country-code': country_code,
                  'keyword': keyword,
                  'size': size,
                  'locale': locale}
        return params

    def capitals_request(self, lang: str):
        choice = {'ua': self.keywords_ua, 'en': self.keywords_en}
        for code, keyword in zip(self.codes, choice[lang]):
            params = self.parameters(code, keyword, 1)
            response = requests.get(self.url, params=params)
            try:
                self.assertIsNotNone(response.json()['items'], msg=f'{response.request.url}')
                # if response.json()['items'] is None:
                #     requested_url = response.request.url
                #     parsed_url = urllib.parse.unquote(requested_url)
                #     print(f"\n{parsed_url}")
                #     print(f"{code}: {keyword}"
                #           f" items: {response.json()['items']}")
            except KeyError:
                print(f"\n{code}: {keyword}")
                print(f'Request: {response.request.url}\n Response: {response.json()}')
                # raise KeyError

    def cities_request(self, lang: str):
        choice = {'ua': self.cities_ua, 'en': self.cities_en}
        for code, keyword in zip(self.codes, choice[lang]):
            params = self.parameters(code, keyword, 1)
            response = requests.get(self.url, params=params)
            try:
                self.assertIsNotNone(response.json()['items'], msg=f'{response.request.url}')
                # if response.json()['items'] is None:
                #     requested_url = response.request.url
                #     parsed_url = urllib.parse.unquote(requested_url)
                #     print(f"\n{parsed_url}")
                #     print(f"{code}: {keyword}"
                #           f" items: {response.json()['items']}")
            except KeyError:
                print(f"\n{code}: {keyword}")
                print(f'Request: {response.request.url}\n Response: {response.json()}')
                # raise KeyError

    def test_eng_capital(self):
        self.capitals_request('en')

    def test_ua_capital(self):
        self.capitals_request('ua')

    def test_eng_cities(self):
        self.cities_request('en')

    def test_ua_cities(self):
        self.cities_request('ua')
