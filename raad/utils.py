from functools import wraps
from django.http import HttpResponseForbidden
from raad.models import AllowedIp


def whitelist_ip(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_ip = request.META.get('REMOTE_ADDR')

        if AllowedIp.objects.filter(ip=user_ip).exists():
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Access denied.")

    return _wrapped_view
