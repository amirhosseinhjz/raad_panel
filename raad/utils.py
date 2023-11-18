from functools import wraps
from django.http import HttpResponseForbidden
from raad.models import AllowedIp
import random


def whitelist_ip(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_ip = request.META.get('HTTP_X_FORWARDED_FOR', '') or request.META.get('REMOTE_ADDR')

        if AllowedIp.objects.filter(ip=user_ip).exists():
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Access denied for ip: " + user_ip)

    return _wrapped_view


def generate_otp():
    return random.randint(1000, 9999)


def normalize_phone(phone):
    return '0' + phone[-10:]
