# Generated by Django 4.2.3 on 2023-07-17 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0003_rename_num_of_mounths_order_num_of_months'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='access_extended',
            field=models.TextField(default='Доступ продлен'),
        ),
        migrations.AddField(
            model_name='settings',
            name='invite_message',
            field=models.TextField(default='Вступайте'),
        ),
    ]