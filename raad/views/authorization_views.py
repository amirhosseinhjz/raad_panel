from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView as BaseLoginView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView


class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('raad:login')
    template_name = 'registration/register.html'


class LoginView(BaseLoginView):
    template_name = 'registration/login.html'

from django.contrib.auth import logout
from django.shortcuts import redirect


def logout_view(request):
    logout(request)
    return redirect('raad:login')
