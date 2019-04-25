import sys
sys.path.append('..')

import unittest
from src.page.login import LoginPage
from selenium.webdriver.common.by import By

class CaseLoginTencentEmail(unittest.TestCase):
    def setUp(self):
        self.url = 'https://mail.qq.com/'
        self.title = '登录QQ邮箱'
        self.driver = None # driver为空时使用配置文件中指定的驱动
        self.page = LoginPage(self.url, self.title, self.driver) 
    
    def tearDown(self):
        self.page.close()

    def test_login(self):
        # logger.info('xxxx')
        # login_page = CaseLoginNetease.page
        self.page.open()
        self.page.switch_frame(self.page.frame_loc)
        self.page.input_username('457624357')
        self.page.input_password('dy12388')
        self.page.click_submit()


if __name__ == '__main__':
    unittest.main()
