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
        input_boxes = self.browser.find_elements(by='tag name', value='input')
        inputbox = [ib for ib in input_boxes if ib.get_attribute('id') == 'id_new_item'][0]
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Новое событие'
        )
        
        # Набираем в текстовом поле "Тестовое событие 1" 
        inputbox.send_keys('Тестовое событие 1')
        # После нажатия Enter, страница обновляется и содержит 
        # "1: Тестовое событие 1"
        inputbox.send_keys(Keys.ENTER)
        time.sleep(2)

        tables = self.browser.find_elements(by='tag name', value='table')
        table = [t for t in tables if t.get_attribute('id') == 'id_events_table'][0]
        rows = table.find_elements(by='tag name', value='tr')
        self.assertIn('1: Тестовое событие 1', [row.text for row in rows])
        
        # Набираем в текстовом поле "Тестовое событие 2"
        # Предлагается ввести событие
        input_boxes = self.browser.find_elements(by='tag name', value='input')
        inputbox = [ib for ib in input_boxes if ib.get_attribute('id') == 'id_new_item'][0]
        inputbox.send_keys('Тестовое событие 2')
        # После нажатия Enter, страница обновляется и содержит 
        # "2: Тестовое событие 2"
        inputbox.send_keys(Keys.ENTER)
        time.sleep(2)

        tables = self.browser.find_elements(by='tag name', value='table')
        table = [t for t in tables if t.get_attribute('id') == 'id_events_table'][0]
        rows = table.find_elements(by='tag name', value='tr')
        self.assertIn('1: Тестовое событие 1', [row.text for row in rows])
        self.assertIn('2: Тестовое событие 2', [row.text for row in rows])

        # Выводится URL с сохраненными событиями
        self.fail('Закончить тест!')

        # Посещаем URL и видим свои два тестовых события


if __name__ == '__main__':
    unittest.main(warnings='ignore')
    