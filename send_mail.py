import smtplib
from email.mime.text import MIMEText
from email.header import Header
def send_mail(msg, sender='Crypto_Billionaire@163.com', receiver='cryptobillionaire@163.com', subject='rush', mail_pass='KJQFLZRODDZEBFKI', mail_host='smtp.163.com'):
    msg = MIMEText(msg)
    msg['From'] = Header('Andy')
    msg['To'] = Header('cryptobillionaire@163.com')
    msg['Subject'] = Header(subject)

    try:
        smtpobj = smtplib.SMTP()
        smtpobj.connect(mail_host, 25)
        smtpobj.login(sender, mail_pass)
        smtpobj.sendmail(sender, receiver, msg.as_string())
        print("sending successfully")
    except smtplib.SMTPException:
        print("failed to send")

if __name__ == "__main__":
    msg = "the crypto billionaire in the future!"
    send_mail(msg)






