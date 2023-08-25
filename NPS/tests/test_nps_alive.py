from basecase import BaseCase
from data.credentials import NPS_URL_PROD


class TestNPSAlive(BaseCase):
    def test_get_nps_url(self):
        response = self.get(NPS_URL_PROD)
        self.assertEqual(response.status_code, 200)
