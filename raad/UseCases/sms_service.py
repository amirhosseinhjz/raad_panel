import requests
from django.conf import settings

OTP_TEMPLATE_ID = 301171
SUCCESSFUL_BUY_TEMPLATE_ID = 700806

WEBSITE_URL = 'my.thundersoftware.net'


def _get_headers():
    return {
        'Accept': 'application/json',
        'X-API-KEY': settings.SMS_API_KEY  # 'l7EhiHbFZ5NObg9zKzKB18VsQADLf7NJLxAiANfmzlHeEjmMPJEYgyn8cS0roR7M'
    }


def send_otp(phone, otp_code):
    data = {
        'Mobile': phone,
        'TemplateId': OTP_TEMPLATE_ID,
        'Parameters': [
            {
                'Name': 'CODE',
                'Value': str(otp_code)
            }
        ]
    }

    return requests.post(url='https://api.sms.ir/v1/send/verify', headers=_get_headers(), json=data).json()


def send_succesful_buy(phone):
    data = {
        'Mobile': phone,
        'TemplateId': SUCCESSFUL_BUY_TEMPLATE_ID,
        'Parameters': [
            {
                'Name': 'WEBPANEL',
                'Value': WEBSITE_URL
            }
        ]
    }

    return requests.post(url='https://api.sms.ir/v1/send/verify', headers=_get_headers(), json=data).json()
