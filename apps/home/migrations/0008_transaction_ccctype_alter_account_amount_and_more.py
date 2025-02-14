# Generated by Django 5.0.6 on 2024-07-13 20:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_remove_transaction_cur_bal'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='cccType',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.acctype'),
        ),
        migrations.AlterField(
            model_name='account',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='cur_bal',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
    ]
