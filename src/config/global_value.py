from pathlib import Path

# 项目的根目录
PROJECT_ROOT = Path(__file__).parents[2]

# 配置文件路径
CONFIG_FILE = PROJECT_ROOT / 'Config/config.ini'

# 驱动路径
DRIVERS_PATH = PROJECT_ROOT / 'Drivers'

# Chrome路径
DRIVER_CHROME = DRIVERS_PATH / 'chromedriver.exe'

# Firefox路径
DRIVER_FIREFOX = DRIVERS_PATH / 'firefox.exe'

# Phantomjs路径
DRIVER_PHANTOMJS = DRIVERS_PATH / 'phantomjs.exe'

# 日志文件目录
LOG_PATH = PROJECT_ROOT / 'Log'

# 测试计划文件路径
PLAN_FILE = PROJECT_ROOT / 'Config/测试计划配置.xlsx'



if __name__ == '__main__':
    print(CONFIG_FILE)