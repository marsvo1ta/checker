import requests

from auth.partners_api_auth import PartnersAuth
from basecase import BaseCase
from auth.enums import *


class TestUser(BaseCase):
    def setUp(self):
        super().setUp()
        self.auth_manager = PartnersAuth()
        self.url = f'{self.auth_manager.url}api/user/'
        self.mail = self.auth_manager.mail
        self.password = self.auth_manager.password
        self.auth_manager.get_token_user()
        self.auth_manager.get_token_back()

    def test_check_user_email(self):
        url = f'{self.url}check_email'
        body = {"email": self.mail}
        auth = self.auth_manager.authorization(USER)
        response = requests.post(url, json=body, headers=auth)
        self.assertEqual(response.json()['message'], 'Authorization by password only')

        body = {"email": "euromobilco_unknown@gmail.com"}
        response = requests.post(url, json=body, headers=auth)
        self.assertEqual(response.json()['message'], 'Password is missing')
        self.assertEqual(response.json()['nextStep'], 'otp')

        body = {"email": "euromobilco_unknown@gmail.com"}
        response = requests.post(url, json=body, headers=auth)
        self.assertEqual(response.json()['message'], 'OTP email has already been sent')

        body = {"email": "eugmail.com"}
        response = requests.post(url, json=body, headers=auth)
        self.assertEqual(response.json()['errors']['email'], 'invalid_email')

    def test_otp_code(self):
        url = f'{self.url}login/otp'
        body = {"email": "euromobilco_unknown@gmail.com",
                "otpCode": "0166"}
        auth = self.auth_manager.authorization(USER)
        response = requests.post(url, json=body, headers=auth)
        result_list = ['The limit of failed OTP code attempts has been reached.'
                       ' Current code has been reset. A new code must be generated.',
                       'OTP code does not match']
        self.assertIn(response.json()['message'], result_list)

        body['email'] = "euromobilco_unknown1@gmail.com"
        response = requests.post(url, json=body, headers=auth)
        self.assertEqual(response.json()['message'], 'Client not found')

        body['email'] = "eugmail.com"
        response = requests.post(url, json=body, headers=auth)
        self.assertEqual(response.json()['errors']['email'], 'invalid_email')

    def test_user_login(self):
        url = f'{self.url}login/password'
        body = {"email": self.mail,
                "password": self.password}
        auth = self.auth_manager.authorization(USER)
        response = requests.post(url, json=body, headers=auth)
        actual_key_list = list(response.json().keys())
        expected_key_list = ['token', 'refreshToken', 'npsCid', 'status', 'message']
        self.assertEqual(actual_key_list, expected_key_list)

        body['password'] = 'Password'
        response = requests.post(url, json=body, headers=auth)
        self.assertEqual(response.json()['message'], 'Incorrect password')

        body['email'] = 'euromobilcogmail.com'
        response = requests.post(url, json=body, headers=auth)
        self.assertEqual(response.json()['errors']['email'], 'invalid_email')

    def test_check_user_password(self):
        url = f'{self.url}check_password'
        body = {"email": self.mail}
        auth = self.auth_manager.authorization(USER)
        response = requests.post(url, json=body, headers=auth)
        self.assertEqual(response.json()['message'], 'Password exist')

        body['email'] = 'euromobilco1@gmail.com'
        response = requests.post(url, json=body, headers=auth)
        self.assertEqual(response.json()['message'], 'Client not found')

        body['email'] = 'euromobilcogmail.com'
        response = requests.post(url, json=body, headers=auth)
        self.assertEqual(response.json()['errors']['email'], 'invalid_email')

        body['email'] = 'euromobilco_unknown@gmail.com'
        response = requests.post(url, json=body, headers=auth)
        self.assertEqual(response.json()['message'], 'Set a password for the user')
        self.assertEqual(response.json()['nextStep'], 'setPassword')

    def test_set_user_password(self):
        url = f'{self.url}set_password'
        body = {
            "email": self.mail,
            "password": self.password,
            "passwordConfirm": self.password
        }
        auth = self.auth_manager.authorization(USER)
        response = requests.put(url, json=body, headers=auth)
        self.assertEqual(response.json()['message'], 'Ok')

        body['passwordConfirm'] = 'Password123'
        response = requests.put(url, json=body, headers=auth)
        self.assertEqual(response.json()['errors']['passwordConfirm'], 'password_not_confirm')

        body = {
            "email": "euromobilcogmail.com",
            "password": "Pa",
            "passwordConfirm": "Pa"
        }
        response = requests.put(url, json=body, headers=auth)
        self.assertEqual(response.json()['errors']['email'], 'invalid_email')
        self.assertEqual(response.json()['errors']['password'], 'value_min_8')
        self.assertEqual(response.json()['errors']['passwordConfirm'], 'value_min_8')

        body = {
            "email": "euromobilco1@gmail.com",
            "password": self.password,
            "passwordConfirm": self.password
        }
        response = requests.put(url, json=body, headers=auth)
        self.assertEqual(response.json()['message'], 'Client not found')

    def test_refresh(self):
        url = f'{self.url}login/password'
        body = {"email": self.mail,
                "password": self.password}
        auth = self.auth_manager.authorization(USER)
        refresh = requests.post(url, json=body, headers=auth).json()['refreshToken']

        url = f'{self.url}token/refresh'
        body = {"refreshToken": refresh}
        response = requests.post(url, json=body)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json()['token'])
        self.assertIsNotNone(response.json()['refreshToken'])

        response = requests.post(url, json=body)
        self.assertEqual(response.status_code, 401)

