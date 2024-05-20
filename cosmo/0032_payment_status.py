# Generated by Django 5.0.4 on 2024-05-15 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osmo', '0031_remove_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('declined', 'Declined')], default='pending', max_length=20),
        ),
    ]
