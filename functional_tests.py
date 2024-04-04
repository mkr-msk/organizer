from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time


class NewVisitorTest(unittest.TestCase):
    'Тест нового посетителя'

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_event_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')

        # Пользователь видит заголовок и шапку сайта
        self.assertIn('Органайзер', self.browser.title)
        header_text = self.browser.find_element(by='tag name', value='h1')
        self.assertIn('События', header_text.text)

        # Предлагается ввести событие
        inputbox = self.browser.find_element(value='id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Новое событие'
        )
        # Набираем в текстовом поле "Тестовое событие 1" 
        inputbox.send_keys('Тестовое событие 1')
        # После нажатия Enter, страница обновляется и содержит 
        # "1: Тестовое событие 1"
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element(value='id_events_table')
        rows = table.find_elements(by='tag name', value='tr')
        self.assertTrue(
            any(row.text == '1: Тестовое событие 1' for row in rows),
            'Новое событие не появилось в таблице'
        )
        # Набираем в текстовом поле "Тестовое событие 2"
        self.fail('Закончить тест!')
        # Выводится URL
        # Посещаем URL и видим свои два тестовых события


if __name__ == '__main__':
    unittest.main(warnings='ignore')