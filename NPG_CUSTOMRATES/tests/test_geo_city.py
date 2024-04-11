import requests
from auth.customrates_auth import CustomRatesAuthManager
from data.credentials import *
from data.country_codes.country_codes import *
from basecase import BaseCase

from typing import Optional


class TestGeo(BaseCase):
    auth_manager: Optional[CustomRatesAuthManager] = None
    auth: Optional[dict] = None
    token: Optional[str] = None
    codes: Optional[list] = None
    keywords_en: Optional[list] = None
    keywords_ua: Optional[list] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.auth_manager = CustomRatesAuthManager('prod')
        cls.auth = cls.auth_manager.auth()
        cls.token = cls.auth_manager.token
        cls.codes = CODES
        cls.keywords_en = KEYWORDS_EN
        cls.keywords_ua = KEYWORDS_UA
        cls.cities_en = CITIES_EN
        cls.cities_ua = CITIES_UA
        cls.url = cls.auth_manager.url


    def form_url(self, code, keyword, size='1'):
        url = f'{self.url}geoCity/{code}?keyword={keyword}&size={size}'
        return url

    def capitals_request(self, lang: str):
        choice = {'ua': self.keywords_ua, 'en': self.keywords_en}
        for code, keyword in zip(self.codes, choice[lang]):
            url = self.form_url(code, keyword)
            response = requests.get(url, headers=self.auth)
            try:
                items = response.json()['items']
            except:
                print(f'\n{code} {keyword}')
                print(f'Request: {url} Response: {response.text}')
            # self.assertIsNotNone(items, msg=f'{code}: {keyword} Не знайдено!!!')

    def cities_request(self, lang: str):
        choice = {'ua': self.cities_ua, 'en': self.cities_en}
        for code, keyword in zip(self.codes, choice[lang]):
            url = self.form_url(code, keyword)
            response = requests.get(url, headers=self.auth)
            try:
                items = response.json()['items']
            except:
                print(f'\n{code} {keyword}')
                print(f'Request: {url} Response: {response.text}')
            # self.assertIsNotNone(items, msg=f'{code}: {keyword} Не знайдено!!!')

    def test_en_capitals(self):
        self.capitals_request('en')

    def test_ua_capitals(self):
        self.capitals_request('ua')

    def test_en_cities(self):
        self.cities_request('en')

    def test_ua_cities(self):
        self.cities_request('ua')

    # def test_1(self):
    #     url = self.url + 'geoCity/ua?keyword=Kyiv&size=1'
    #     response = requests.get(url, headers=self.auth)
    #     if response.json()['message'] == 'Forbidden':
    #         print(self.auth_manager.key)