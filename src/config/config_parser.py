from configparser import ConfigParser, NoSectionError, NoOptionError
from src.config.global_value import CONFIG_FILE, PLAN_FILE


class Config:
    def __init__(self, config_file=CONFIG_FILE):
        self.parser = self.__config_parse(config_file)

    @property
    def driver_type(self):
        return self.__get_option('PROJECT', 'driverType', 'Chrome')

    
    @property
    def time_out(self):
        return self.__get_option('TEST', 'timeOut', 10)
    

    @property
    def is_head_less(self):
        return self.__get_option('TEST', 'isHeadLess', False)
    
    @property
    def plan_file_path(self):
        return self.__get_option('TEST', 'planFilePath', PLAN_FILE)

    
    @property
    def is_send_email(self):
        return self.__get_option('EMAIL', 'isSendEmail', False)

    
    @property
    def smtp_username(self):
        return self.__get_option('EMAIL', 'SMTPUserName', '')

    
    @property
    def smtp_password(self):
        return self.__get_option('EMAIL', 'SMTPPassword', '')

    
    @property
    def smtp_server_address(self):
        return self.__get_option('EMAIL', 'SMTPServerAddress', '')


    @property
    def sender_name(self):
        return self.__get_option('EMAIL', 'senderName', '')


    @property
    def sender_address(self):
        return self.__get_option('EMAIL', 'senderAddress', '')
    

    @property
    def smtp_port(self):
        return int(self.__get_option('EMAIL', 'SMTPPort', 587))
    

    @property
    def email_title(self):
        return self.__get_option('EMAIL', 'emailTitle', 'Web自动化测试报告')
    

    @property
    def email_text(self):
        return self.__get_option('EMAIL', 'emailText', '详细测试报告请查看附件...')
    

    @property
    def receivers_address(self):
        address = self.parser.items(section='receiversAddress')  
        return [v.split(', ') for v in dict(address).values()]


    @property
    def report_title(self):
        return self.__get_option('REPORT', 'title', '测试报告')


    @property
    def report_description(self):
        return self.__get_option('REPORT', 'description', '')


    def __config_parse(self, config_file):
        parser = ConfigParser()
        parser.read(filenames=config_file, encoding='utf-8')
        return parser


    def __get_option(self, section, option, default_value):
        try:
            value = self.parser.get(section=section, option=option)
        except(NoSectionError, NoOptionError):
            # 默认值
            value = default_value
            # log
            # logger.warning('config.ini文件未配置%s.%s选项，采用默认值“%s”' % (section, option, default_value))
        return value
    
    def get_section(self, section):
        return dict(self.parser.items(section=section))


# class LogConfig(Config):
#     def __init__(self):
#         super().__init__()
#         self.__section = self.get_section('LOG')
#         self.path = self.__section['savepath']
#         self.level = self.__section['logginglevel']



# 单例
config = Config()
# log_config = LogConfig()
# print(log_config.log_path)