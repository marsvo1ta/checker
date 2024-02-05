from auth.partners_api_auth import PartnersAuth
from basecase import BaseCase


class TestLogin(BaseCase):
    def setUp(self):
        super().setUp()
        self.auth_manager = PartnersAuth()
        self.auth_manager.get_token_back()
        self.auth_manager.get_token_user()

    def test_auth(self):

        self.assertIsNotNone(self.auth_manager.back_token)
        self.assertIsNotNone(self.auth_manager.user_token)
