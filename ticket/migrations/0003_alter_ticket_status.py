# Generated by Django 4.2.5 on 2023-11-02 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0002_alter_ticket_options_alter_ticketreply_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('open', 'باز'), ('closed', 'بسته شده'), ('in_progress', 'در دست اقدام')], default='open', max_length=20),
        ),
    ]