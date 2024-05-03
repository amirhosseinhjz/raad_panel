from django_cron import CronJobBase, Schedule
from raad.UseCases.get_new_orders import get_new_orders
from django.contrib.auth.models import User
from raad import models
from raad.config import PRODUCT_COMPANY_DURATION_CONFIG
from datetime import datetime, timedelta
from raad.utils import normalize_phone


class SyncFromWooCommerceCronJob(CronJobBase):
    RUN_EVERY_MINUTES = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINUTES)

    code = 'raad.sync_from_woocommerce'

    def do(self):
        try:
            while orders := get_new_orders():
                for order in orders:
                    user = self.get_or_create_user(order)
                    for order_item in order['items']:
                        self.create_data(order_item, user)
        except Exception as e:
            error = models.ErrorLog()
            error.source = 'sync_data_from_woocommerce'
            error.error_message = str(e)
            error.save()
            raise e

    @staticmethod
    def get_or_create_user(order_data):
        email = order_data['order_user_email']
        phone = normalize_phone(order_data['order_user_phone'])

        if user := User.objects.filter(username=phone).first():
            if user.email is None:
                user.email = email
                user.save()
            return user

        if user := User.objects.filter(email=email).first():
            # if user.profile.phone is None:
            #     user.profile.phone = phone
            #     user.save()
            return user

        user = User.objects.create_user(username=phone, email=email, password=phone)
        user.save()
        return user

    @staticmethod
    def create_data(order_item_data, user):
        try:
            company = models.Company.objects.get(user=user)
        except models.Company.DoesNotExist:
            company = models.Company.objects.create(
                user=user,
                expiration_date=datetime.now() + timedelta(days=365)
            )

        quantity = int(order_item_data['qty'])

        devices = []
        for _ in range(quantity):
            device = models.Device.objects.create(
                company=company,
                notify_for_created=False
            )
            devices.append(device)
        # send_mail(from_email=settings.DEFAULT_FROM_EMAIL, subject='گروه نرم افزاری رعد-سفارش موفق', message=texts.SUCCESSFUL_EMAIL_MESSAGE,
        #           recipient_list=[company.user.email], fail_silently=True)
        # send_succesful_buy(company.user.username, fail_silently=True)

    @staticmethod
    def create_company(order_item_data, user):
        product_id = int(order_item_data['product_id'])
        quantity = int(order_item_data['qty'])

        if not product_id in PRODUCT_COMPANY_DURATION_CONFIG:
            error = models.ErrorLog()
            error.source = 'sync_orders_from_woocommerce'
            error.error_message = f"invalid product {product_id}, " + str(order_item_data)
            error.save()
            return

        duration = PRODUCT_COMPANY_DURATION_CONFIG[product_id]

        for _ in range(quantity):
            # TODO: maybe just adding device is needed
            company = models.Company()
            company.user = user
            company.expiration_date = datetime.now() + timedelta(days=duration)
            company.save()
