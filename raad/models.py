from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class AllowedIp(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=64, unique=True)


class Client(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    expiration_date = models.DateTimeField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="companies")

    def has_expired(self):
        return self.expiration_date < timezone.now()


class Device(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    license_key = models.CharField(max_length=200, unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="devices")


class MessengerAdmin(models.Model):
    MESSENGER_CHOICES = [
        ('bale', 'Bale'),
        ('telegram', 'Telegram'),
    ]

    id = models.AutoField(primary_key=True)
    messenger = models.CharField(max_length=16, choices=MESSENGER_CHOICES)
    admin_messenger_id = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="admins")


