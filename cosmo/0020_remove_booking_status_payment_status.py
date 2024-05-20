# Generated by Django 5.0.4 on 2024-05-09 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osmo', '0019_alter_payment_total'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='status',
        ),
        migrations.AddField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('declined', 'Declined')], default='pending', max_length=20),
        ),
    ]
