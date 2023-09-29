from django import forms
from raad.models import MessengerAdmin
from .models import Device


class MessengerAdminForm(forms.ModelForm):
    class Meta:
        model = MessengerAdmin
        fields = ['messenger', 'admin_messenger_id']


class DeviceNameUpdateForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['name']
