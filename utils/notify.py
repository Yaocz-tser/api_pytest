#发送邮件
import re
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import logging

def parse_smtp_uri(conf_uri):
    if conf_uri is None:
        raise TypeError('conf_uri参数不能为None')
    try:
        smtp_type, user, password, host, port = re.split(r'://|:|@|/', conf_uri)
    except ValueError:
        (r'db_uri:{conf_uri} - 格式不正确，参数格式:SMTP_URI=smtp://user:password@smpt_server:port')

    is_ssl = 'ssl' in smtp_type
    user = f'{user}@{".".join(host.split(".")[1:])}'
    port = int(port) if port else None
    smtp_conf = dict(host=host,port=port,is_ssl=is_ssl,user=user,password=password)
    print(smtp_conf)
    return smtp_conf


class Email:
    def __init__(self,smtp_conf=None):
        #self.smtp_conf = smtp_conf or parse_smtp_uri(os.getenv('SMTP_URI'))
        self.smtp_conf = smtp_conf or parse_smtp_uri('smtp_ssl://297219420:lhhhgcnjkovgbjfj@smtp.qq.com:25')
        self.msg = MIMEMultipart()
        self.smtp = None

    def smtp_login(self):
        is_ssl = self.smtp_conf.get('is_ssl',False)
        host = self.smtp_conf.get('host')
        user = self.smtp_conf.get('user')
        password = self.smtp_conf.get('password')
        port = self.smtp_conf.get('port')
        if is_ssl:
            self.smtp = smtplib.SMTP_SSL(host)
        else:
            self.smtp = smtplib.SMTP(host,port)
        self.smtp.login(user,password)

    def add_body(self,body,html=False):
        if html:
            self.msg.attach(MIMEText(body,'html','utf-8'))
        else:
            self.msg.attach(MIMEText(body,'plain','utf-8'))
    
    def add_attachment(self,file_path):
        attachment = MIMEText(open(file_path,'rb').read(),'base64','utf-8')
        attachment['Content-Type'] = 'application/octet-stream'
        attachment['content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
        self.msg.attach(attachment)

    def add_header(self,receivers,subject):
        self.msg['From'] = self.smtp_conf.get('user')
        self.msg['To'] = receivers
        self.msg['Subject'] = subject

    def send(self,subject,receivers,body,file_path,html=False):
        '''
        发送邮件
        subject:邮件主题
        receivers：收件人列表
        body:正文信息
        file_path:附件路径
        
        '''
        self.add_body(body,html)
        self.add_header(receivers,subject)
        self.add_attachment(file_path)
        self.smtp_login()        
        logging.debug(f'发送邮件给: {receivers}')
        self.smtp.sendmail(self.smtp_conf.get('user'), receivers, self.msg.as_string())
        logging.info('邮件发送成功')



if __name__ == "__main__":
    Email().send('接口测试报告','yaoczz@foxmail.com','test')