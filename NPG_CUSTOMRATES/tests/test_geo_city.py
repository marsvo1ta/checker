import requests
from auth.customrates_auth import CustomRatesAuthManager
from data.credentials import *
from data.country_codes.country_codes import *
from basecase import BaseCase

from typing import Optional


class TestCalculate(BaseCase):
    auth_manager: Optional[CustomRatesAuthManager] = None
    auth: Optional[dict] = None
    token: Optional[str] = None
    codes: Optional[list] = None
    keywords_en: Optional[list] = None
    keywords_ua: Optional[list] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.auth_manager = CustomRatesAuthManager(CUSTOMRATES_AUTH_STAGE,
                                                  CUSTOMRATES_CLIENT_ID_STAGE,
                                                  CUSTOMRATES_CLIENT_SECRET_STAGE)
        cls.auth = cls.auth_manager.auth()
        cls.token = cls.auth_manager.token
        cls.codes = CODES
        cls.keywords_en = KEYWORDS_EN
        cls.keywords_ua = KEYWORDS_UA
        cls.cities_en = CITIES_EN
        cls.cities_ua = CITIES_UA

    def form_url(self, code, keyword, size='1'):
        url = f'https://api.dev.customsrates.com/geoCity/{code}?keyword={keyword}&size={size}'
        return url

    def capitals_request(self, lang: str):
        choice = {'ua': self.keywords_ua, 'en': self.keywords_en}
        for code, keyword in zip(self.codes, choice[lang]):
            if code == 'sg' or code == 'tr':
                print(f'{code}: {keyword} Не знайдено!!!')
                continue
            url = self.form_url(code, keyword)
            response = requests.get(url, headers=self.auth)
            items = response.json()['items']
            r = response.json()
            if not items:
                print(f'\n{url}')
                print(f'{response.request.url}')
                print(f"{code} {keyword}\n{r}")
                if 'ʼ' in keyword:
                    print('Тут апостроф')

    def cities_request(self, lang: str):
        choice = {'ua': self.cities_ua, 'en': self.cities_en}
        for code, keyword in zip(self.codes, choice[lang]):
            if code in ['sg', 'tr']:
                print(f'{code}: {keyword} Не знайдено!!!')
                continue
            url = self.form_url(code, keyword)
            response = requests.get(url, headers=self.auth)
            self.assertIsNotNone(response.json()['items'])
            items = response.json()['items']
            r = response.json()
            if not items:
                # print(f'\n{response.request.url}')
                print(f'\n{url}')
                print(f"{code} {keyword}\n{r}")
                if 'ʼ' in keyword:
                    print('Тут апостроф')

    def test_en_capitals(self):
        self.capitals_request('en')

    def test_ua_capitals(self):
        self.capitals_request('ua')

    def test_en_cities(self):
        self.cities_request('en')

    def test_ua_cities(self):
        self.cities_request('ua')

