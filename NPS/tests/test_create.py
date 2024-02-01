import random

import pytest
from seleniumbase import BaseCase


def random_number(start: int = 1, stop: int = 9) -> int:
    return random.randrange(start, stop)


def contains(tag: str, value: str) -> str:
    return f"{tag}:contains('{value}')"


def dropdown(find: str, tag: str = 'li') -> str:
    return contains(tag, find)


class TestCreate(BaseCase):

    @pytest.mark.run(order=1)
    def test_login(self):
        self.open('https://air.nova.global/login')
        self.type('#email', 'marsvolta@ukr.net')
        self.type('#password', 'Password1')
        self.click('.checkbox-element')
        self.click('.btn.btn_primary.btn_full')
        self.save_cookies('stage_login.txt')

    @pytest.mark.run(order=2)
    def test_create_order(self,
                     country: str = 'США',
                     store: str = 'eBay',
                     category: str = 'Голка'):
        self.open('https://air.nova.global/')
        self.load_cookies('stage_login.txt')
        self.open('https://air.nova.global/orders')
        self.click('.cabinet-link')
        self.click('div#vs1__combobox')
        self.click(dropdown(country))
        if country == 'США':
            self.click('//*[@id="add-order"]/div/div/div[5]/div/div/div[4]/span')
        self.click('#vs2__combobox')
        self.click(dropdown(store))
        self.type("input[aria-labelledby='vs4__combobox']", category)
        self.click(dropdown(category))
        self.type('#forward_order_name', 'Test')
        self.type('#forward_order_items_0_name', 'Test')
        self.type('#forward_order_items_0_unitPrice_tbbc_amount', '1')
        self.type('#forward_order_trackNo', f'Test_{random_number(123411, 999991)}')
        self.click('button#declaration')
        h2 = contains('h2', 'Адреса отримання')
        self.wait_for_element(h2)
        register_button = contains('button', 'Зареєструвати відправлення')
        self.assert_text('Зареєструвати відправлення', register_button)
        while self.is_element_visible(h2) or self.is_element_visible(register_button):
            self.sleep(1)
            self.click(register_button)
            self.wait_for_element_absent(register_button)
        h1 = contains('h1', 'Відправлення успішно додано')
        self.wait_for_element(h1)
        cabinet_button = self.find_element('a.btn.btn_outline')
        while self.is_element_visible(h1):
            cabinet_button.click()
            self.sleep(1)

if __name__ == '__main__':
    pytest.main()