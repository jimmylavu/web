# Generated by Django 5.0.4 on 2024-05-20 06:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('osmo', '0065_booking_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='phone',
        ),
    ]
