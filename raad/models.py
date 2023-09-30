from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class AllowedIp(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.ip


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    license_key = models.CharField(max_length=200, unique=True)
    expiration_date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="companies")

    def save(self, *args, **kwargs):
        if not self.name:
            company_count = self.user.companies.count()
            self.name = f'شرکت {company_count + 1}'

        if not self.license_key:
            self.license_key = str(uuid.uuid4())[:30]

        super(Company, self).save(*args, **kwargs)

        if not self.devices.exists():
            device = Device()
            device.company = self
            device.save()

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
    is_activated = models.BooleanField(default=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="devices")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name:
            devices_count = self.company.devices.count()
            self.name = f'دستگاه {devices_count + 1}'

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
