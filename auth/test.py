import requests


def test_get_token_back(self):
    basic_auth = (self.basic_login, self.basic_password)
    body = {"login": "test_test",
            "password": "Password1"}

    response = requests.post(self.back_auth_url,
                             auth=basic_auth,
                             json=body)
    print(response.text)