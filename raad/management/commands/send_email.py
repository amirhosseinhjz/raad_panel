from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from raad.UseCases.get_new_orders import get_new_orders
from raad.crons.notify_user_for_purchase import NotifyUserNewPurchaseCronJob
from raad.models import Company, Device


class Command(BaseCommand):
    help = 'Send email'

    def handle(self, *args, **kwargs):
        # from raad.crons.sync_full_data_to_servers import SyncFullDataToServersCronJob
        #
        # SyncFullDataToServersCronJob().do()
        # data = get_new_orders()
        #
        # print(data)
        company = Company.objects.all()[0]
        device = Device.objects.all()[0]

        NotifyUserNewPurchaseCronJob.send_purchase_email(company, [device], 'amexhjz@gmail.com')
