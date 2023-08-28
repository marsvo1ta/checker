from basecase import BaseCase
from data.credentials import NPG_URL_PROD, NPG_URL_STAGE
from auth.authorization import AuthManager


class TestNPG(BaseCase):
    def setUp(self):
        super().setUp()
        self.auth_manager = AuthManager()

    def test_get_warehouses(self):
        response = self.get(f'{NPG_URL_PROD}warehouses', headers=self.auth_manager.prod_admin_auth())
        total = response.json()['metadata']['total']
        self.assertGreater(total, 83_000, f'total = {total} statuscode = {response.status_code}')

    def test_get_poland_warehouses(self):
        params = {'filter[country.code]': 'PL'}
        response = self.get(f'{NPG_URL_PROD}warehouses', headers=self.auth_manager.prod_admin_auth(), params=params)
        total = response.json()['metadata']['total']
        self.assertGreater(total, 60_000, f'total = {total} statuscode = {response.status_code}')

    def test_get_poland_warehouses_by_partner_id(self):
        params = {'filter[country.code]': 'PL', 'filter[partnerId]': '[176|95]'}
        response = self.get(f'{NPG_URL_PROD}warehouses', headers=self.auth_manager.prod_admin_auth(), params=params)
        total = response.json()['metadata']['total']
        self.assertGreater(total, 20_000, f'total = {total} statuscode = {response.status_code}')

    def test_get_poland_branches_by_partner_id(self):
        params = {'filter[country.code]': 'PL', 'filter[partnerId]': '[176|95]',
                  'filter[pointType]': 'branch'}
        response = self.get(f'{NPG_URL_PROD}warehouses', headers=self.auth_manager.prod_admin_auth(), params=params)
        total = response.json()['metadata']['total']
        self.assertGreater(total, 1, f'total = {total} statuscode = {response.status_code}')

    def test_get_poland_lockers_by_partner_id(self):
        params = {'filter[country.code]': 'PL', 'filter[partnerId]': '[176|95]',
                  'filter[pointType]': 'locker'}
        response = self.get(f'{NPG_URL_PROD}warehouses', headers=self.auth_manager.prod_admin_auth(), params=params)
        total = response.json()['metadata']['total']
        self.assertGreater(total, 20_000, f'total = {total} statuscode = {response.status_code}')
