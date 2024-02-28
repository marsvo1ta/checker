from pprint import pprint

import requests

from auth.partners_api_auth import PartnersAuth
from basecase import BaseCase
from auth.enums import *


class TestOrder(BaseCase):
    def setUp(self):
        super().setUp()
        self.auth_manager = PartnersAuth()
        self.url = f'{self.auth_manager.url}api/partners/order/'
        self.mail = self.auth_manager.mail
        self.password = self.auth_manager.password
        self.auth_manager.get_token_user()
        self.auth_manager.get_token_back()

    def create_body_json(self) -> dict:
        body = {
            "npsCid": "NP000541130",
            "trackNumber": self.generate_tracking_number(),
            "name": "Testing",
            "promoCode": "buyout_percent",
            "senderCountryCode": "US",
            "shop": {
                "name": "Bluetti",
                "id": 655
            },
            "deliveryPoint": {
                "branchRef": "1ec09d88-e1c2-11e3-8c4a-0050568002cf"
            },
            "goods": [
                {
                    "name": "Test_product",
                    "quantity": 1,
                    "pricePerUnit": 1.99,
                    "currency": "USD",
                    "hsCode": "7323990000"
                }
            ],
            "document": {
                "firstName": "Олег",
                "middleName": "Вікторович",
                "lastName": "Котигорошко",
                "birthDate": "1995-01-30",
                "docType": "id",
                "docNumber": "00000001",
                "issueDate": "2010-01-30",
                "issueBy": "1234",
                "registrationAddress": "example",
                "itin": "0000000001",
                "invoice": "https://ds8zc8d02ynm5.cloudfront.net/documents/invoices/65ba1091e384c.png"
            }
        }
        return body

    def edit_track_json(self):
        body = {
            "npsCid": "NP000541130",
            "orderNumber": "NP70000002422696NPGSTAG",
            "trackNumber": "TBT494490876111"
        }
        return body

    def list_orders_json(self):
        body = {
            "npsCid": "NP000541130",
            "page": 1,
            "size": 20,
            "filters": {
                "source": "api",
                "state": [
                    "draft",
                    "process",
                    "received",
                    "archived",
                    "returned"
                ]
            }
        }
        return body

    def test_valid_create(self):
        auth = self.auth_manager.authorization(BACK)
        body = self.create_body_json()
        url = f'{self.url}create'
        response = requests.post(url, json=body, headers=auth)
        self.assertTrue(response.status_code == 200)


    def test_invalid_delivery_point(self):
        auth = self.auth_manager.authorization(BACK)
        body = self.create_body_json()
        url = f'{self.url}create'
        body.update({"deliveryPoint": {
            "branchRef": "1ec09d88-e1c2-11e3-8c4a-0050568002c"}})
        response = requests.post(url, json=body, headers=auth)
        self.assertEqual(response.json()['errors']['deliveryPoint.branchRef'], "Об'єкт не існує")


    def test_add_track_number_valid(self):
        url = f'{self.url}track/number'
        body = self.edit_track_json()
        auth = self.auth_manager.authorization(BACK)
        response = requests.post(url, json=body, headers=auth)
        self.assertEqual(response.json()['status'], 'success')

    def test_add_track_number_invalid(self):
        url = f'{self.url}track/number'
        track = self.edit_track_json()
        track['trackNumber'] = 'TBA094490827610'
        auth = self.auth_manager.authorization(BACK)
        headers = {'Accept': 'application/json'}
        headers.update(auth)
        response = requests.post(url, json=track, headers=headers)
        self.assertEqual(response.json()['errorDescription'],
                         "Відправлення з даним трек-номером уже було створено.")

        track['trackNumber'] = '12345'
        response = requests.post(url, json=track, headers=headers)
        self.assertEqual(response.json()['errors']['trackNumber'],
                         "Значення занадто коротке. Повинно бути рівне 6 символам або більше.")

        track.update({'trackNumber': self.generate_tracking_number(), 'npsCid': 'NP000541128'})
        response = requests.post(url, json=track, headers=headers)
        self.assertEqual(response.status_code, 403)

    def test_list_orders(self):
        body = self.list_orders_json()
        url = f'{self.url}list'
        auth = self.auth_manager.authorization(BACK)
        response = requests.post(url, json=body, headers=auth)
        length = len(response.json()['items'])
        self.assertGreater(length, 11)

        body['size'] = 10
        response = requests.post(url, json=body, headers=auth)
        self.assertEqual(response.json()['errors']['size'], 'range_20_40')

        body['size'] = 50
        response = requests.post(url, json=body, headers=auth)
        self.assertEqual(response.json()['errors']['size'], 'range_20_40')

        body = self.list_orders_json()
        body['filters']['source'] = 'site'
        response = requests.post(url, json=body, headers=auth)
        pagination = response.json()['page']
        total_items = pagination['totalItems']
        self.assertGreater(total_items, 194)
        page = pagination['totalPages'] - 1
        last_page_page_items = total_items - (page * 20)

        body['page'] = pagination['totalPages']
        response = requests.post(url, json=body, headers=auth)
        count_items = len(response.json()['items'])
        self.assertEqual(count_items, last_page_page_items)

        body['filters']['state'] = ['draft']
        response = requests.post(url, json=body, headers=auth)
        self.assertTrue(response.json()['page']['totalItems'] != 0)
