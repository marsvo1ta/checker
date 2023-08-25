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
