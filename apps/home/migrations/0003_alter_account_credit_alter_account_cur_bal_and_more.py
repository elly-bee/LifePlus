# Generated by Django 5.0.6 on 2024-07-13 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_acctype_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='credit',
            field=models.IntegerField(blank=True, default=1),
        ),
        migrations.AlterField(
            model_name='account',
            name='cur_bal',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='debit',
            field=models.IntegerField(blank=True, default=-1),
        ),
    ]
