# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import traceback
import loggers

logger = loggers.get_logger()

To = ["rd@yottabyte.cn", "presale@yottabyte.cn", "postsale@yottabyte.cn"]
Cc = ["chen.jun@yottabyte.cn"]
# To = ["751948630@qq.com"]
# Cc = ["hu_minghao@outlook.com"]


def send_email(subject, content):
    smtp_server = "smtp.exmail.qq.com"
    username = "tools@yottabyte.cn"
    password = "UtOiRnil&.4Co"
    # username = "hu.minghao@yottabyte.cn"
    # password = "Hmh931028*"

    chenbao_ad = u"\n\n------------------------------------------------\n" \
                 u"晨报易 - 晨报处理更容易  http://192.168.1.160:8012 "

    if not isinstance(subject, unicode):
        subject = unicode(subject)
    if not isinstance(content, unicode):
        content = unicode(content)
    if not isinstance(chenbao_ad, unicode):
        chenbao_ad = unicode(chenbao_ad)
    From = "%s<%s>" % (Header('晨报易', 'utf-8'), username)

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = From
    msg["To"] = ",".join(To)
    msg["Cc"] = ",".join(Cc)
    msg["Accept-Language"] = "zh-CN"
    msg["Accept-Charset"] = "ISO-8859-1,utf-8"

    body = MIMEText(content + chenbao_ad, 'plain', 'utf-8')
    msg.attach(body)

    try:
        smtp = smtplib.SMTP()
        smtp.connect(smtp_server)
        smtp.login(username, password)
        smtp.sendmail(From, To + Cc, msg.as_string())
        smtp.quit()
        rc = 0
    except Exception:
        logger.error(traceback.format_exc())
        rc = 1

    return rc
