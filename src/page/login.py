from selenium.webdriver.common.by import By
from src.page.base import BasePage

class LoginPage(BasePage):
    frame_loc = (By.XPATH, '//*[@id="login_frame1"]')
    qqlogin_loc = (By.XPATH, '//*[@id="qqLoginTab"]')
    username_loc = (By.XPATH, '//*[@id="u"]')
    password_loc = (By.XPATH, '//*[@id="p"]')
    submit_loc = (By.XPATH, '//*[@id="login_button"]')

    # def __init__(self, url, title, driver):
    #     if driver:
    #         super().__init__(url, title, driver)
    #     else:
    #         super().__init__(url, title)


    def input_username(self, username):
        self.send_keys(self.username_loc, username, clear=False, click=False)
    
    def input_password(self, password):
        self.send_keys(self.password_loc, password)
    
    def click_submit(self):
        self.click(self.submit_loc)
