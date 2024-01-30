import requests
from basecase import BaseCase
from data.credentials import NPG_DDC_PROD


class TestClassification(BaseCase):

    def setUp(self):
        super().setUp()
        self.url = f'{NPG_DDC_PROD}search/cargo?country-code=ua&size=100&fuzzy=true&locale=uk&keyword='

    def test_ddc_ua(self):
        keywords_list = ['куртка', 'шорти', 'мʼяч', 'штани']
        for idx, word in enumerate(keywords_list):
            request_url = f'{self.url}{word}'
            response = requests.get(request_url)
            items = response.json()['items']
            keyword = items[0]['keywords']['currentLocal']
            self.assertIsNotNone(items, word)
            self.assertIn(word, keyword.lower().replace('\'', 'ʼ'))

    def test_ddc_us(self):
        keywords_list = ['coat', 'shorts', 'ball', 'pants']
        self.url = self.url.replace('locale=uk', 'locale=en')
        for idx, word in enumerate(keywords_list):
            request_url = f'{self.url}{word}'
            response = requests.get(request_url)
            items = response.json()['items']
            keyword = items[0]['keywords']['currentLocal']
            self.assertIsNotNone(response.json().get('items'), word)
            self.assertIn(word, keyword.lower().replace('\'', 'ʼ'))

    def test_ddc_pl(self):
        keywords_list = ['kurtka', 'spodenki', 'piłka', 'spodnie']
        self.url = self.url.replace('locale=uk', 'locale=pl')
        for idx, word in enumerate(keywords_list):
            request_url = f'{self.url}{word}'
            response = requests.get(request_url)
            items = response.json()['items']
            keyword = items[0]['keywords']['currentLocal']
            self.assertIsNotNone(response.json().get('items'), word)
            self.assertIn(word, keyword.lower().replace('\'', 'ʼ'))

    def test_ddc_hs_code_us(self):
        hs_code_list = ['9503009900', '9405119090', '6405909000', '9506620000']
        dots_hs_code_list = self.set_dots_to_hs_codes(hs_code_list)
        category_list = ['Kids products', 'House, cottage and garden',
                         'Footwear And Accessories', 'Sports, fitness and hobbies']
        self.url = self.url.replace('locale=uk', 'locale=en')

        for category, hscode, dots_hscode in zip(category_list, hs_code_list, dots_hs_code_list):
            dots_url = f'{self.url}{dots_hscode}'
            request_url = f'{self.url}{hscode}'
            response = requests.get(request_url)
            dots_response = requests.get(dots_url)
            items = response.json().get('items')
            category_en = items[0]['category']['en']
            hs_code = f'{items[0]["hsCode"]}'
            dots_hs_code = dots_response.json().get('items')[0]['hsCode']
            self.assertIsNotNone(items)
            self.assertEqual(hscode, hs_code)
            self.assertEqual(category, category_en)
            self.assertEqual(dots_hs_code, hscode)

    def test_ddc_hs_code_ua(self):
        hs_code_list = ['9503009900', '9405119090', '6405909000', '9506620000']
        dots_hs_code_list = self.set_dots_to_hs_codes(hs_code_list)
        category_list = ['Товари для дітей', 'Дім, дача і сад',
                         'Взуття та аксесуари', 'Спорт, фітнес та хобі']

        for category, hscode, dots_hscode in zip(category_list, hs_code_list, dots_hs_code_list):
            dots_url = f'{self.url}{dots_hscode}'
            request_url = f'{self.url}{hscode}'
            response = requests.get(request_url)
            dots_response = requests.get(dots_url)
            items = response.json().get('items')
            category_en = items[0]['category']['currentLocal']
            hs_code = f'{items[0]["hsCode"]}'
            dots_hs_code = dots_response.json().get('items')[0]['hsCode']
            self.assertIsNotNone(items)
            self.assertEqual(hscode, hs_code)
            self.assertEqual(category, category_en)
            self.assertEqual(dots_hs_code, hscode)

    def test_pagination(self):
        """Not Implemented"""
        pass

