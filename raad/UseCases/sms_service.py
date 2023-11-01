import requests
from django.conf import settings
from raad.models import ErrorLog

OTP_TEMPLATE_ID = 301171
SUCCESSFUL_BUY_TEMPLATE_ID = 700806

WEBSITE_URL = 'my.thundersoftware.net'


def _get_headers():
    return {
        'Accept': 'application/json',
        'X-API-KEY': settings.SMS_API_KEY
    }


def send_otp(phone, otp_code, fail_silently=False):
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

    try:
        return requests.post(url='https://api.sms.ir/v1/send/verify', headers=_get_headers(), json=data).json()
    except Exception as e:
        ErrorLog.objects.create(
            source='send_order_email',
            error_message=str(e),
        )
        if not fail_silently:
            raise e


def send_succesful_buy(phone, fail_silently=False):
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
    try:
        return requests.post(url='https://api.sms.ir/v1/send/verify', headers=_get_headers(), json=data).json()
    except Exception as e:
        ErrorLog.objects.create(
            source='send_order_email',
            error_message=str(e),
        )
        if not fail_silently:
            raise e
