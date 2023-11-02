from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
from datetime import datetime, timedelta


class ConfigModel(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=200, unique=True)
    value = models.CharField(max_length=200)

    def __str__(self):
        return self.key


class SyncServerUrl(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=200, unique=True)


class AllowedIp(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.ip


class ErrorLog(models.Model):
    source = models.TextField()
    error_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class SyncDataAPI(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('success', 'Success'),
        # ('failed', 'Failed'),
    )
    REQUEST_METHOD_CHOICES = (
        ('get', 'Get'),
        ('post', 'Post'),
    )

    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=200)
    data = models.TextField()
    method = models.CharField(max_length=20, choices=REQUEST_METHOD_CHOICES, default='get')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.url


class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    generated_at = models.DateTimeField(auto_now=True)


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    license_key = models.CharField(max_length=200, unique=True)
    expiration_date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="companies")
    demo = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['expiration_date']),
            models.Index(fields=['license_key']),
        ]

    def save(self, *args, **kwargs):
        if not self.name:
            company_count = self.user.companies.count()
            self.name = f'شرکت {company_count + 1}'

        if self.demo and not self.id:
            self.expiration_date = datetime.now() + timedelta(days=7)

        if not self.license_key:
            self.license_key = str(uuid.uuid4())[:34].replace('-', '')

        super(Company, self).save(*args, **kwargs)

        # if not self.devices.exists():
        #     device = Device()
        #     device.company = self
        #     device.save()

    def has_expired(self):
        return self.expiration_date < timezone.now()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "شرکت ها"
        verbose_name = "شرکت"


class Device(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    device_id = models.CharField(max_length=200, blank=True, default='')
    sub_id = models.IntegerField(blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="devices")
    notify_user = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        devices_count = self.company.devices.count()
        if not self.name:
            self.name = f'دستگاه {devices_count + 1}'

        if not self.sub_id:
            self.sub_id = devices_count + 1
        super(Device, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "دستگاه ها"
        verbose_name = "دستگاه"


class MessengerAdmin(models.Model):
    MESSENGER_CHOICES = [
        ('bale', 'Bale'),
        ('telegram', 'Telegram'),
    ]

    id = models.AutoField(primary_key=True)
    messenger = models.CharField(max_length=16, choices=MESSENGER_CHOICES)
    admin_messenger_id = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="admins")

    def __str__(self):
        return f'{self.messenger} {self.admin_messenger_id}'

    class Meta:
        verbose_name_plural = "مدیرهای پیامرسان"
        verbose_name = "مدیر پیامرسان"


