# Generated by Django 4.2.3 on 2023-07-17 16:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='num_of_mounths',
            new_name='num_of_months',
        ),
    ]