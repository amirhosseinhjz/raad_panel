from django.db.models.signals import post_save
from django.dispatch import receiver
from raad.models import Company, Device, MessengerAdmin, SyncServerUrl, ErrorLog, SyncDataAPI
from raad.UseCases.data_provider import get_company_full_data
import json


@receiver(post_save, sender=Company)
def company_post_save(sender, instance, created, **kwargs):
    if created:
        return
    data = get_company_full_data(instance)
    sync_company(data)


@receiver(post_save, sender=Device)
def device_post_save(sender, instance, created, **kwargs):
    company = instance.company
    data = get_company_full_data(company)
    sync_company(data)


@receiver(post_save, sender=MessengerAdmin)
def messenger_admin_post_save(sender, instance, created, **kwargs):
    company = instance.company
    data = get_company_full_data(company)
    sync_company(data)


def sync_company(data):
    data = data if isinstance(data, str) else json.dumps(data)

    for server_model in SyncServerUrl.objects.all():
        url = server_model.url

        SyncDataAPI.objects.create(
            url=url,
            data=data
        )
