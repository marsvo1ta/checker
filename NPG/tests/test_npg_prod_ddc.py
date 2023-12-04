import requests
from basecase import BaseCase
from data.credentials import NPG_DDC_PROD


class TestCalculate(BaseCase):

    def setUp(self):
        super().setUp()
        self.url = f'{NPG_DDC_PROD}search/cargo?country-code=ua&locale=uk&keyword='

    def test_ddc_ua(self):
        keywords_list = ['куртка', 'шорти', 'мʼяч', 'штани']
        for idx, word in enumerate(keywords_list):
            request_url = f'{self.url}{word}'
            response = requests.get(request_url)
            self.assertIsNotNone(response.json()['items'], word)

    def test_ddc_us(self):
        keywords_list = ['coat', 'shorts', 'ball', 'pants']
        self.url = self.url.replace('locale=uk', 'locale=en')
        for idx, word in enumerate(keywords_list):
            request_url = f'{self.url}{word}'
            response = requests.get(request_url)
            self.assertIsNotNone(response.json()['items'], word)

    def test_ddc_pl(self):
        keywords_list = ['kurtka', 'spodenki', 'piłka', 'spodnie']
        self.url = self.url.replace('locale=uk', 'locale=pl')
        for idx, word in enumerate(keywords_list):
            request_url = f'{self.url}{word}'
            response = requests.get(request_url)
            self.assertIsNotNone(response.json()['items'], word)
