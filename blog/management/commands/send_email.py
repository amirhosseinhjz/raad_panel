from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Send email'

    # def add_arguments(self, parser):
    #     parser.add_argument('post_id', type=int, help='ID of the BlogPost to duplicate')
    #     parser.add_argument('count', type=int, help='Number of times to duplicate the BlogPost')

    def handle(self, *args, **kwargs):
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        # Email configurations
        sender_email = 'raad@mohammadbna.ir'
        receiver_email = 'amexhjz@gmail.com'
        password = 'K}H5y6nH_eoT'
        subject = 'Subject here'
        message = 'Here is the message.'

        smtp_server = 'mail.mohammadbna.ir'  # Replace with your cPanel SMTP server
        smtp_port = 587  # Use the appropriate SMTP port

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        # Send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print('Email sent successfully.')
