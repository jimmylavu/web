# Generated by Django 5.0.4 on 2024-05-09 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osmo', '0023_payment_timestamp_delete_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.IntegerField(null=True),
        ),
    ]