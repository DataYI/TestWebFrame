from selenium import webdriver
from src.config.config_parser import config
from src.config.global_value import DRIVER_CHROME, DRIVER_PHANTOMJS, DRIVER_FIREFOX
from src.exception.config_exception import ConfigException

# drivers_map = {
#     'Chrome': webdriver.Chrome
# }

driver_type = config.driver_type.capitalize()
# driver = getattr(webdriver, driver_type, webdriver.Chrome)()
DRIVER = None
if driver_type == 'Chrome':
    DRIVER = webdriver.Chrome(DRIVER_CHROME.as_posix())
elif driver_type == 'Firefox':
    DRIVER = webdriver.Firefox(DRIVER_FIREFOX.as_posix())
elif driver_type == 'Phantomjs':
    DRIVER = webdriver.PhantomJS(DRIVER_PHANTOMJS.as_posix())
else:
    raise ConfigException('配置文件中指定的Driver类型：%s不存在对应的驱动程序！' % driver_type)