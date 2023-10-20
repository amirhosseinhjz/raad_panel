from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from raad.models import Company, Device, MessengerAdmin, ServiceServerIp, ErrorLog
from raad.UseCases.data_provider import get_company_full_data


@receiver(post_save, sender=Company)
def company_post_save(sender, instance, created, **kwargs):
    if created:
        pass
#     TODO: send email


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
    for ip_model in ServiceServerIp.objects.all():
        ip = ip_model.ip
        url = f"https://{ip}/your-endpoint"

        try:
            response = requests.post(url, json=data, timeout=10)
            if response.status_code != 200:
                ErrorLog.objects.create(
                    source=url,
                    error_message=str(response.status_code) + ' ' + response.json()
                )
        except requests.exceptions.RequestException as e:
            ErrorLog.objects.create(
                source=url,
                error_message=str(e)
            )
