# Generated by Django 5.0.4 on 2024-05-03 06:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osmo', '0003_rename_monthly_id_monthly_quantity_monthly_mop_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Installment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='plan',
            name='installment',
        ),
        migrations.AddField(
            model_name='plan',
            name='install_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='osmo.installment'),
        ),
    ]