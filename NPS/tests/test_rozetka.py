from seleniumbase import BaseCase


class TestRozetka(BaseCase):
    def test_rozetka(self):
        self.open('https://rozetka.com.ua/ua/adidas_4062051415369/p178636109/')
        text = self.get_text('button.button.button--medium.button--navy.ng-star-inserted')
        is_available = text == "Повідомити, коли з'явиться"
        if is_available:
            print("send")