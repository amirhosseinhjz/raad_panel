import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


sender_email = 'raad@mohammadbna.ir'
password = 'K}H5y6nH_eoT'
smtp_server = 'mail.mohammadbna.ir'
smtp_port = 587


def send_email(receiver_email, **kwargs):

    subject = kwargs.get('subject', '')
    message = kwargs.get('message', '')

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        try:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        except Exception as e:
            pass
            # TODO: log error
