from django_cron import CronJobBase, Schedule
from raad.UseCases.get_new_orders import get_new_orders
from django.contrib.auth.models import User
from raad import models
from raad.config import PRODUCT_COMPANY_DURATION_CONFIG
from datetime import datetime, timedelta


class SyncDataToServersCronJob(CronJobBase):
    RUN_EVERY_MINUTES = 30

    schedule = Schedule(run_every_mins=RUN_EVERY_MINUTES)

    code = 'raad.sync_data_to_servers'

    def do(self):
        for item in models.SyncDataAPI.objects.filter(status='pending'):
            url = item.url
            payload = item.payload
            try:
                response = requests.post(url, data=payload)
                if response.status_code == 200:
                    item.status = 'success'
                    item.save()
                    continue

                error_message = response.json()
            except requests.exceptions.RequestException as e:
                error_message = str(e)

            models.ErrorLog.objects.create(
                source=url,
                error_message=error_message,
            )
