from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    'Тест нового посетителя'

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_event_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')

        self.assertIn('Organizer', self.browser.title)
        self.fail('Закончить тест!')

        # Предлагается ввести событие
        # Набираем в текстовом поле "Тестовое событие 1" 
        # Набираем в текстовом поле "Тестовое событие 2"
        # Выводится URL
        # Посещаем URL и видим свои два тестовых события


if __name__ == '__main__':
    unittest.main(warnings='ignore')