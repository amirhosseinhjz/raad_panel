from django import forms
from raad.models import MessengerAdmin
from .models import Device, Company


class MessengerAdminForm(forms.ModelForm):
    class Meta:
        model = MessengerAdmin
        fields = ['messenger', 'admin_messenger_id']


class DeviceUpdateForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['name']


class CompanyUpdateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name']


class CompanyAdminForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['license_key'].required = False
