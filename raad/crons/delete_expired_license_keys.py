from django_cron import CronJobBase, Schedule
from raad.models import Company, SyncDataAPI, SyncServerUrl
from datetime import datetime, timedelta


class DeleteExpiredLicenseKeysCronJob(CronJobBase):
    RUN_EVERY_DAYS = 24 * 60

    schedule = Schedule(run_every_mins=RUN_EVERY_DAYS)

    code = 'raad.delete_expired_license_keys'

    def do(self):
        from_date = self.get_from_date()

        companies = Company.objects.filter(
            expiration_date__lt=from_date
            ).filter(deleted=False
            ).filter(demo=True)

        for company in companies:
            company.deleted = True
            company.save()

    @staticmethod
    def sync_data(company):
        DELETE_COMPANY_URI = '/panel/DeleteClient/'
        for server_model in SyncServerUrl.objects.all():
            url = server_model.url + DELETE_COMPANY_URI + company.license_key

            SyncDataAPI.objects.create(
                url=url,
                method='get'
            )

    @staticmethod
    def get_from_date():
        return datetime.now()
