# Generated by Django 5.0.4 on 2024-05-11 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osmo', '0025_paymentreminder'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='remaining_balance',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='total_payable',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
