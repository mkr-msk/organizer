from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time, os


MAX_WAIT = 10

class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                tables = self.browser.find_elements(by='tag name', value='table')
                table = [t for t in tables if t.get_attribute('id') == 'id_events_table'][0]
                rows = table.find_elements(by='tag name', value='tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(1)
        
    def test_can_start_a_list_for_one_user(self):
        self.browser.get(self.live_server_url)

        # Пользователь видит заголовок и шапку сайта
        self.assertIn('Органайзер', self.browser.title)
        header_text = self.browser.find_element(by='tag name', value='h1')
        self.assertIn('Начать новый список', header_text.text)

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
        time.sleep(1)
        self.wait_for_row_in_list_table('1: Тестовое событие 1')
        
        # Набираем в текстовом поле "Тестовое событие 2"
        # Предлагается ввести событие
        input_boxes = self.browser.find_elements(by='tag name', value='input')
        inputbox = [ib for ib in input_boxes if ib.get_attribute('id') == 'id_new_item'][0]
        inputbox.send_keys('Тестовое событие 2')
        # После нажатия Enter, страница обновляется и содержит 
        # "2: Тестовое событие 2"
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.wait_for_row_in_list_table('1: Тестовое событие 1')
        self.wait_for_row_in_list_table('2: Тестовое событие 2')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url)
        input_boxes = self.browser.find_elements(by='tag name', value='input')
        inputbox = [ib for ib in input_boxes if ib.get_attribute('id') == 'id_new_item'][0]
        inputbox.send_keys('Тестовое событие 1')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.wait_for_row_in_list_table('1: Тестовое событие 1')

        user1_list_url = self.browser.current_url
        self.assertRegex(user1_list_url, '/events/.+')

        self.browser.quit()
        self.browser = webdriver.Firefox()

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(by='tag name', value='body').text
        self.assertNotIn('Тестовое событие 1', page_text)
        self.assertNotIn('Тестовое событие 2', page_text)

        input_boxes = self.browser.find_elements(by='tag name', value='input')
        inputbox = [ib for ib in input_boxes if ib.get_attribute('id') == 'id_new_item'][0]
        inputbox.send_keys('Тестовое событие 3')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.wait_for_row_in_list_table('1: Тестовое событие 3')

        user2_list_url = self.browser.current_url
        self.assertRegex(user2_list_url, '/events/.+')
        self.assertNotEqual(user2_list_url, user1_list_url)

        page_text = self.browser.find_element(by='tag name', value='body').text
        self.assertNotIn('Тестовое событие 1', page_text)
        self.assertIn('Тестовое событие 3', page_text)

    def test_layout_and_styling(self):

        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1920, 1080)

        input_boxes = self.browser.find_elements(by='tag name', value='input')
        inputbox = [ib for ib in input_boxes if ib.get_attribute('id') == 'id_new_item'][0]
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            630,
            delta=10
        )

        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.wait_for_row_in_list_table('1: testing')
        input_boxes = self.browser.find_elements(by='tag name', value='input')
        inputbox = [ib for ib in input_boxes if ib.get_attribute('id') == 'id_new_item'][0]
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            630,
            delta=10
        )
