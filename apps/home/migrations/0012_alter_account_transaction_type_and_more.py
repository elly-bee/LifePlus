# Generated by Django 5.0.6 on 2024-07-13 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_alter_account_transaction_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='transaction_type',
            field=models.IntegerField(choices=[(1, 'Credit'), (-1, 'Debit')], default=1),
        ),
        migrations.AlterField(
            model_name='transaction_codes',
            name='transaction_type',
            field=models.IntegerField(choices=[(1, 'Credit'), (-1, 'Debit')]),
        ),
    ]
