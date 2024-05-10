from django_cron import CronJobBase, Schedule
from raad.UseCases.get_new_orders import get_new_orders
from django.contrib.auth.models import User
from raad import models
from raad.config import *
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
                    self.process_order(order)
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

    def process_order(self, order):
        user = self.get_or_create_user(order)
        company_order_item = None
        for order_item in order['items']:
            if order_item["product_id"] in COMPANY_PRODUCT_IDS:
                company_order_item = order_item
        company = self.get_or_create_company(company_order_item, user)
        self.create_devices(order, company)

    @staticmethod
    def get_or_create_company(company_order_item, user):
        try:
            company = models.Company.objects.get(user=user)
        except models.Company.DoesNotExist:
            company = None

        # if company is not None and not company.has_expired() and company_order_item is not None:
        #     error_message = f"User {user} has active company but new company order item received with data {company_order_item}"
        #     models.ErrorLog.objects.create(
        #         source='sync_from_woocommerce',
        #         error_message=error_message
        #     )
        #     return company
        product_id = company_order_item["product_id"]
        duration_in_days = PRODUCT_COMPANY_DURATION_CONFIG.get(product_id, None)
        if duration_in_days is None:
            models.ErrorLog.objects.create(
                source='sync_orders_from_woocommerce',
                error_message=f"invalid product {product_id}, {company_order_item}"
            )
            return

        now = datetime.now()

        if company is None:
            company = models.Company(user=user, expiration_date=now)

        if company.expiration_date < now:
            company.expiration_date = now

        company.expiration_date = company.expiration_date + timedelta(days=duration_in_days)
        company.save()
        return company

    def create_devices(self, order, company):
        for order_item in order['items']:
            if order_item["product_id"] in DEVICE_PRODUCT_IDS:
                quantity = int(order_item['qty'])

                for _ in range(quantity):
                    device = models.Device.objects.create(
                        company=company,
                        notify_for_created=False
                    )
