# Generated by Django 3.2.11 on 2023-10-10 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0025_auto_20231010_0646'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='enter_your_phone',
            field=models.TextField(default='Пожалуйста введите ваш номер'),
        ),
    ]
