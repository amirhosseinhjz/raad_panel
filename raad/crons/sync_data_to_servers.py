from django_cron import CronJobBase, Schedule
from raad import models
import requests


class SyncDataToServersCronJob(CronJobBase):
    RUN_EVERY_MINUTES = 15

    schedule = Schedule(run_every_mins=RUN_EVERY_MINUTES)

    code = 'raad.sync_data_to_servers'

    def do(self):
        for item in models.SyncDataAPI.objects.filter(status='pending'):
            url = item.url
            payload = item.data
            try:
                response = requests.post(url, headers=self.get_headers(), data=payload)
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

    @staticmethod
    def get_headers():
        return {
            'Content-Type': 'application/json'
        }