from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        #self.browser.quit()
        self.browser.close()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('To-Do',self.browser.title)
        heaer_text = self.browser.find_elements_by_tag_name('h1').text
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

        # 待办事项表格中显示了"1: Buy peacok feathers"
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy peacok feathers' for row in rows)
        )

        # 页面中又显示了一个文本框，可以输入其他的代办事项
        # 她输入了"Use peacock feathers to make a fly"
        # 伊迪斯做事很有条理
        self.fail('Finish the test!')

        # 页面再次更新，她的清单中显示了这两个待办事项

if __name__ == '__main__':
    unittest.main(warnings='ignore')
