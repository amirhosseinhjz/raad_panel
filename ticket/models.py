from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=[
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('in_progress', 'In Progress'),
    ], default='open')

    def __str__(self):
        status_choices = {
            'open': 'باز',
            'closed': 'بسته',
            'in_progress': 'در حال انجام',
        }
        status_str = status_choices.get(self.status.__str__(), 'نامشخص')
        return f"{self.title} ({status_str}) {self.created_by.username}"

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "تیکت ها"
        verbose_name = "تیکت"


class TicketReply(models.Model):
    id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='replies')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()

    def __str__(self):
        return f"پاسخ توسط {self.created_by} در تاریخ {self.created_at}"

    class Meta:
        verbose_name_plural = "پاسخ تیکت ها"
        verbose_name = "پاسخ تیکت"
