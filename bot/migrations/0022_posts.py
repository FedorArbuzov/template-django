# Generated by Django 4.2.3 on 2023-09-20 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0021_profile_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(default='У вас новый материал')),
                ('sent', models.BooleanField(default=False)),
            ],
        ),
    ]
