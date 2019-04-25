from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from src.config.driver_config import DRIVER
from src.utils.log import Logger

logger = Logger().get_logger()

class BasePage:
    def __init__(self, url, title, driver):
        if driver:
            self.driver = driver
        else:
            self.driver = DRIVER
        self.url = url
        self.title = title

    def _open(self, url, title):
        '''
        打开并校验页面是否正确加载
        '''
        self.driver.get(url)
        self.driver.maximize_window()
        assert self.is_on_page(title), '打开页面出错，url: %s' % url
    
    def find_element(self, loc):
        '''
        重写元素定位方法
        '''
        try:
            WebDriverWait(self.driver, 10).until(lambda driver: driver.find_element(*loc).is_displayed())
            return self.driver.find_element(*loc)
        except (NoSuchElementException, TimeoutException):
            logger.error('“%s”页面中未找到%s元素' % (self.title, loc))
    
    def switch_frame(self, loc):
        return self.driver.switch_to.frame(self.find_element(loc))

    def open(self):
        self._open(self.url, self.title)
    
    def close(self):
        self.driver.close()

    def quit(self):
        self.driver.quit()

    def click(self, loc):
        self.find_element(loc).click()

    def exec_script(self, script):
        '''
        执行指定的js脚本
        '''
        self.driver.execute_script(script)
    
    def send_keys(self, loc, value, click=True, clear=True):
        '''
        重写send_keys方法
        '''
        el = self.find_element(loc)
        if click:
            el.click()
        if clear:
            el.clear()
        el.send_keys(value)


    def is_on_page(self, title):
        '''
        判断页面标题是否符合期望
        '''
        return title in self.driver.title