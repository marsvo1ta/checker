import requests
from basecase import BaseCase
from data.credentials import NPG_DDC_PROD

translations = {
    "uk": "Одяг",  # Українська
    "pl": "piłka",  # Польська
    "ro": "minge",  # Румунська
    "en": "ball",  # Англійська
    "de": "Ball",  # Німецька
    "lt": "kamuolys",  # Литовська
    "es": "pelota",  # Іспанська
    "fr": "balle",  # Французька
    "it": "palla",  # Італійська
    "et": "pall",  # Естонська
    "hu": "labda",  # Угорська
}


class TestClassificationLocales(BaseCase):

    def setUp(self):
        super().setUp()
        self.url = f'{NPG_DDC_PROD}search/cargo?country-code=ua&size=1'

    def test_locations(self):
        for idx, (country_code, translation) in enumerate(translations.items(), start=1):
            params = {'keyword': translation, 'locale': country_code}
            response = requests.get(self.url, params=params)
            self.assertGreaterEqual(response.json()['pagination']['total'], 1, msg=response.request.url)

