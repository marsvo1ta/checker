import requests as r
from data.credentials import *


def test_alive():
    response = r.get(NPS_URL_PROD)
    assert response.status_code == 200
    