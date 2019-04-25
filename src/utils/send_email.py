import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from pathlib import Path
from src.config.config_parser import config


def create_msg(sender: list, receivers: list, subj: str, content: str, file: Path) -> MIMEMultipart:
    '''
    创建消息体对象
    :s_form: 发件人，包括姓名和邮件地址
    :receivers: 收件人，嵌套列表，内层列表包括姓名和邮件地址
    :subj: 邮件主题
    :content: 邮件内容
    :filename: 附件文件路径
    '''
    msg = MIMEMultipart()
    msg['From'] = formataddr(sender)
    for receiver in receivers:
        msg['To'] = formataddr(receiver)
    msg['Subject'] = subj
    msg.attach(MIMEText(content, _subtype='plain', _charset='utf-8'))
    # 附件
    attach = MIMEText(open(file, 'rb').read(), 'base64', 'utf-8')   
    attach['Content-Type'] = 'application/octet-stream'  
    attach.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', file.name))
    msg.attach(attach)
    return msg


def send_mail(msg: MIMEMultipart, smtp: tuple, from_addr: str, password: str, to_addr: list) -> None:
    '''
    发送邮件
    :msg: 消息对象
    :smtp: smtp服务器地址与端口
    :from_addr: 发件账户
    :password: 发件账户密码
    :to_addr: 收件人地址列表
    '''
    try:
        server = smtplib.SMTP(*smtp)
        server.starttls()
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit
        print('邮件发送成功')
    except Exception:
        print(msg['To'] + '的邮件发送失败')


def send_report(report_path: Path) -> None:
    '''
    通过配置文件中的信息用邮件发送指定的报告文件
    :report_path: 测试报告文件的路径
    '''
    cfg = Config()
    # smtp服务器地址与端口
    smtp = (cfg.smtp_server_address, cfg.smtp_port)
    #email地址与密码
    from_addr = cfg.smtp_username
    password = cfg.smtp_password
    # #收件人地址列表，配置文件中包含了收件人名称和地址，这里只需要地址
    to_addr = [addr[1] for addr in cfg.receivers_address]

    # 发件人
    sender = [cfg.sender_name, cfg.sender_address]
    # 收件人列表，一个嵌套列表，内层列表包含了收件人名称和地址两个元素
    receivers = cfg.receivers_address

    # 邮件主题
    subj = cfg.email_title
    content = cfg.email_text

    # 构造消息体
    msg = create_msg(sender, receivers, subj, content, report_path)
    # 发送邮件
    send_mail(msg, smtp, from_addr, password, to_addr)





