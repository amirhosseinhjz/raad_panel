# Generated by Django 4.2.5 on 2023-09-30 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_blogpostimage_remove_blogpost_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogpost',
            options={'ordering': ['-priority', '-pub_date'], 'verbose_name': 'پست', 'verbose_name_plural': 'پست ها'},
        ),
        migrations.AlterModelOptions(
            name='blogpostimage',
            options={'verbose_name': 'عکس', 'verbose_name_plural': 'عکس ها'},
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='is_pinned',
        ),
        migrations.AddField(
            model_name='blogpost',
            name='priority',
            field=models.IntegerField(default=0),
        ),
    ]
