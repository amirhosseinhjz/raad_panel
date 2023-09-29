from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class AllowedIp(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=64, unique=True)


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    expiration_date = models.DateTimeField()
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="companies")

    def has_expired(self):
        return self.expiration_date < timezone.now()

    def get_devices_count(self):
        return self.devices.count()

    class Meta:
        verbose_name_plural = "شرکت ها"
        verbose_name = "شرکت"


class Device(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    license_key = models.CharField(max_length=200, unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="devices")

    def save(self, *args, **kwargs):
        if not self.license_key:
            self.license_key = str(uuid.uuid4())[:30]

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

    class Meta:
        verbose_name_plural = "مدیرهای پیامرسان"
        verbose_name = "مدیر پیامرسان"

