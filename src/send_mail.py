from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from config import USERNAME_YANDEX_MAIL, PASSWORD_YANDEX_MAIL
# login = "scriptForm@yandex.ru"
# password = "6626553000d"

def add_file_mail(marketpalce):
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(f"../result_parse/{marketpalce}.xlsx", "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"'%(f"{marketpalce}.xlsx"))
    return part

def seng_mail(to_addr, subject):
    msg = MIMEMultipart()
    msg['From'] = USERNAME_YANDEX_MAIL
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg.attach(add_file_mail("Ozon"))
    msg.attach(add_file_mail("Wildberries"))
    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    server.ehlo(USERNAME_YANDEX_MAIL)
    server.login(USERNAME_YANDEX_MAIL, PASSWORD_YANDEX_MAIL)
    server.auth_plain()
    server.send_message(msg)
    server.quit()