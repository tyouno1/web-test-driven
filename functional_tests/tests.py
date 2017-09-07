from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from contextlib import contextmanager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of

from django.test import LiveServerTestCase
import unittest

#class NewVisitorTest(unittest.TestCase):
class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        #self.browser.quit()
        self.browser.close()

    @contextmanager
    def wait_for_page_load(self, timeout=30):
        old_page = self.browser.find_element_by_tag_name("html")
        yield WebDriverWait(self.browser, timeout).until(
            staleness_of(old_page)
        )

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        #self.browser.get('http://localhost:8000')
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do',self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
       
        # 应用邀请她输入一个待办事项
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # 她按了回车键后，页面更新了
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)

        ## 待办事项表格中显示了"1: Buy peacok feathers"
        #table = self.browser.find_element_by_id('id_list_table')
        #rows = table.find_elements_by_tag_name('tr')
        ##self.assertTrue(
        ##    any(row.text == '1: Buy peacok feathers' for row in rows),
        ##    "New to-do item did not appear in table -- its text was:\n%s" %(table.text,)
        ##)

        #self.assertIn('1: Buy peacock feathers', [row.text for row in rows])
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        with self.wait_for_page_load(timeout=10):
            self.check_for_row_in_list_table('1: Buy peacock feathers')
        
        # 页面中又显示了一个文本框，可以输入其他的代办事项
        # 她输入了"Use peacock feathers to make a fly"
        # 伊迪斯做事很有条理
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # 页面再次刷新，清单中显示了两个待办事项
        #table = self.browser.find_element_by_id('id_list_table')
        #rows = table.find_elements_by_tag_name('tr')
        #self.assertIn('1: Buy peacock feathers', [row.text for row in rows])
        #self.assertIn(
        #    '2: Use peacock feathers to make a fly' ,
        #    [row.text for row in rows]
        #)
        with self.wait_for_page_load(timeout=10):
            self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
            self.check_for_row_in_list_table('1: Buy peacock feathers')

        # 确保伊迪斯的信息不会从cookie中泄露出来
        self.browser.close()


        # 又有一个叫弗朗西斯的用户访问了这个网站
        # 页面中应该看不到伊迪斯的清单
        self.browser = webdirver.Firefox()
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers',page_text)
        self.assertNotIn('make a fly',page_text)

        # 弗朗西斯输入一个待办事项，新建一个清单
        inputbox = self.browser.find_elemet_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # 弗朗西斯获得了他唯一的URL
        francis_list_url = self.browser.current_url

        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        ####
        self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
