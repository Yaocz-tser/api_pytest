import os
import pytest
import allure
from datetime import datetime
from utils.notify import Email

#初始化
def pytest_configure(config):
    if config.getoption('htmlpath'):  
        now = datetime.now().strftime('%Y%m%d_%H%M%S')
        config.option.htmlpath = os.path.join(config.rootdir, 'reports', f'report_{now}.html')

#添加命令行参数
def pytest_addoption(parser):
    parser.addoption('--send-email',action='store_true',help='发送邮件')
    parser.addini('email_subject',help='邮件主题')
    parser.addini('email_receivers',help='收件人')
    parser.addini('email_body','邮件正文')

#发送邮件
def pytest_terminal_summary(config):
    send_email = config.getoption('--send-email')
    email_receivers = config.getini('email_receivers')
    if send_email is True and email_receivers:
        report_path = config.getoption('htmlpath')
        email_subject = config.getini('email_subject') or 'TestReport'
        email_body = config.getini('email_body') or 'HI'
        
        if email_receivers:
            Email().send(email_subject,email_receivers,email_body,report_path)

#失败截图
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        mode = "a" if os.path.exists("failures") else "w"
        with open("failures", mode) as f:
            if "tmpdir" in item.fixturenames:
                extra = " ({})".format(item.funcargs["tmpdir"])
            else:
                extra = ""

            f.write(rep.nodeid + extra + "\n")
        with allure.step('添加失败截图'):
            allure.attach('截图方法', "失败截图", allure.attachment_type.PNG)
