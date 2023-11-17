from django_cron import CronJobBase, Schedule
from raad.models import Company, Device
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from raad.UseCases.sms_service import send_succesful_buy
from django.db import transaction


class NotifyUserNewPurchaseCronJob(CronJobBase):
    RUN_EVERY_MINS = 5

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)

    code = 'raad.notify_user_new_purchase'

    def do(self):
        self.send_for_companies()
        self.send_for_devices()

    @staticmethod
    def send_for_companies():
        companies = Company.objects.filter(notify_for_created=True)

        for company in companies:
            devices = company.devices.filter(notify_for_created=True)

            NotifyUserNewPurchaseCronJob.send_purchase_email(company, devices, company.user.email)
            send_succesful_buy(company.user.username)

            with transaction.atomic():
                company.notify_for_created = False
                company.save()
                for device in devices:
                    device.notify_for_created = False
                    device.save()

    @staticmethod
    def send_for_devices():
        devices_to_notify = Device.objects.filter(notify_for_created=True)

        for device in devices_to_notify:
            company = device.company
            devices = Company.devices.filter(notify_for_created=True)

            if not devices:
                continue

            NotifyUserNewPurchaseCronJob.send_purchase_email(company, devices, company.user.email)
            send_succesful_buy(company.user.username)

            with transaction.atomic():
                company.notify_for_created = False
                company.save()
                for _device in devices:
                    _device.notify_for_created = False
                    _device.save()

    @staticmethod
    def send_purchase_email(company, devices, email):
        context = {
            'company': company,
            'devices': devices,
        }
        html_content = render_to_string('mail/successful_order.html', context)
        send_mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            subject='گروه نرم افزاری رعد-سفارش موفق',
            message='',
            html_message=html_content,
            recipient_list=[email],
            fail_silently=False
        )
