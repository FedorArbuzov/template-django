# Generated by Django 4.2.3 on 2023-08-11 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0008_settings_file_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='settings',
            name='invite_message',
        ),
        migrations.AddField(
            model_name='settings',
            name='invite_message_channel',
            field=models.TextField(default='Вступайте в канал'),
        ),
        migrations.AddField(
            model_name='settings',
            name='invite_message_group',
            field=models.TextField(default='Вступайте в группу'),
        ),
    ]
