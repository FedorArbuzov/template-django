# Generated by Django 4.2.3 on 2023-08-11 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0005_rename_num_of_months_order_subscribe_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tariff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('price', models.IntegerField(default=500)),
            ],
        ),
    ]
