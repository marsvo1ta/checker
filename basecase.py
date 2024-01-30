import unittest
import requests


class BaseCase(unittest.TestCase):
    def setUp(self):
        self.session = requests.Session()

    def tearDown(self):
        self.session.close()

    def get(self, url, **kwargs):
        return self.session.get(url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self.session.post(url, data=data, json=json, **kwargs)

    def set_dots_to_hs_codes(self, hs_codes):
        formatted_codes = []

        for hs_code in hs_codes:
            formatted_code = "{}.{}.{}".format(hs_code[:4], hs_code[4:6], hs_code[6:])
            formatted_codes.append(formatted_code)

        return formatted_codes

