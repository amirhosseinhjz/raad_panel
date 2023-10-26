from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView as BaseLoginView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from raad.utils import generate_otp
from raad.models import OTP
from raad.UseCases import sms_service
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.contrib import messages


class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('raad:login')
    template_name = 'registration/register.html'


class LoginView(BaseLoginView):
    template_name = 'registration/login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        otp = request.POST.get('otp')

        if password:
            user = authenticate(username=username, password=password)
            if user is None:
                messages.error(request, 'اطلاعات نامعتبر')
                return redirect('raad:login')
            login(request, user)
            return redirect('raad:dashboard')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return redirect('raad:login')

        user_otp = OTP.objects.get(user=user)

        if user_otp and user_otp.otp_code == otp and (timezone.now() - user_otp.generated_at).total_seconds() < 120:
            login(request, user)
            return redirect('raad:dashboard')

        messages.error(request, 'کد نامعتبر')
        return redirect('raad:login')


def logout_view(request):
    logout(request)
    return redirect('raad:login')


@require_POST
def send_otp(request):
    body = json.loads(request.body)
    username = body.get('username', None)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        response_data = {'message': 'کاربر پیدا نشد!'}
        return JsonResponse(response_data, status=404)

    otp_code = generate_otp()

    OTP.objects.update_or_create(user=user, defaults={'otp_code': otp_code})

    sms_service.send_otp(user.username, otp_code)

    response_data = {}
    return JsonResponse(response_data)
