# Generated by Django 4.2.3 on 2023-08-11 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0013_settings_close_channel_btn_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='buy_channel_btn',
            field=models.TextField(default='Тариф «Святая база» 1 490 Р'),
        ),
    ]
