from django.db.models.signals import post_save
from django.dispatch import receiver
from raad.models import Company, Device, MessengerAdmin, SyncServerUrl, ErrorLog, SyncDataAPI
from raad.UseCases.data_provider import get_company_full_data
import json
from raad.UseCases import sms_service
from django.core.mail import send_mail
from django.conf import settings
from raad.UseCases import texts


@receiver(post_save, sender=Company)
def company_post_save(sender, instance, created, **kwargs):
    # if created:
    #     sms_service.send_succesful_buy(instance.user.username)
    data = get_company_full_data(instance)
    sync_company(data)


@receiver(post_save, sender=Device)
def device_post_save(sender, instance, created, **kwargs):
    # if created and instance.notify_user:
    #     sms_service.send_succesful_buy(instance.company.user.username, fail_silently=True)
    #     if email := instance.company.user.email:
    #         send_mail(from_email=settings.DEFAULT_FROM_EMAIL, subject='گروه نرم افزاری رعد-سفارش موفق', message=texts.SUCCESSFUL_EMAIL_MESSAGE, recipient_list=[email], fail_silently=True)
    company = instance.company
    data = get_company_full_data(company)
    sync_company(data)


@receiver(post_save, sender=MessengerAdmin)
def messenger_admin_post_save(sender, instance, created, **kwargs):
    company = instance.company
    data = get_company_full_data(company)
    sync_company(data)


SYNC_COMPANY_URI = '/panel/SendClient'


def sync_company(data):

    data = data if isinstance(data, str) else json.dumps(data)

    for server_model in SyncServerUrl.objects.all():
        url = server_model.url + SYNC_COMPANY_URI

        SyncDataAPI.objects.create(
            url=url,
            data=data,
            method='post'
        )
