# Generated by Django 5.0.4 on 2024-05-18 11:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osmo', '0049_remove_booking_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentreminder',
            name='transaction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='osmo.transaction'),
        ),
    ]
