import requests

basic_login = str('nova_post')
basic_password = str('Hg71FjI95hB3aS0L')
url = 'https://npshopping-stag.c1.npshopping.com/api/partners/login'


def test_get_token_back():
    basic_auth = (basic_login, basic_password)
    body = {"login": "test_test",
            "password": "Password1"}
    response = requests.post(url,
                             auth=basic_auth,
                             json=body)
    json_response = response.json()
    print(json_response.get('token'))