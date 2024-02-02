from auth.partners_api_auth import PartnersAuth
from basecase import BaseCase


class TestLogin(BaseCase):
    def setUp(self):
        super().setUp()
        self.auth_manager = PartnersAuth()


    def test_auth(self):
        print(f'AUTH: {self.auth_manager.get_token_back()}')
        # print(f'AUTH: {self.auth_user}')
        # self.assertIsNotNone(self.auth_user)
        # self.assertIsNotNone(self.auth_back)
