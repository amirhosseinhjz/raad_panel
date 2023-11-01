from django_cron import CronJobBase, Schedule
import requests
from raad import models
from django.core.paginator import Paginator
from raad.models import Company
from raad.UseCases.data_provider import get_company_full_data


class SyncFullDataToServersCronJob(CronJobBase):
    RUN_EVERY_DAYS = 3 * 24 * 60

    schedule = Schedule(run_every_mins=RUN_EVERY_DAYS)

    code = 'raad.sync_full_data_to_servers'

    def do(self):
        try:
            all_companies = Company.objects.all().order_by('id')
            paginator = Paginator(all_companies, 1000)

            page_number = 1
            while page_number <= paginator.num_pages:
                companies_page = paginator.page(page_number)
                company_list = []
                for company in companies_page.object_list:
                    data = get_company_full_data(company)
                    company_list.append(data)
                models.ErrorLog.objects.create(
                    source='full_data_log',
                    error_message=str(company_list)
                )

                for server in models.SyncServerUrl.objects.all():
                    self.send_data(server.url, company_list)

                page_number += 1
        except Exception as e:
            models.ErrorLog.objects.create(
                source='sync_full_data_to_servers',
                error_message=str(e)
            )
            raise e

    def send_data(self, url, data):
        url = url + '/panel/SendAllClients'
        try:
            requests.post(url=url, json=data)
        except requests.exceptions.RequestException as e:
            models.ErrorLog.objects.create(
                source='send full data to: ' + url,
                error_message=str(e),
            )
