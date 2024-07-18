# Generated by Django 5.0.6 on 2024-07-13 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_alter_account_desc_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='transaction_type',
            field=models.IntegerField(choices=[('Credit', 'Credit'), ('Debit', 'Debit')], default=1),
        ),
        migrations.AlterField(
            model_name='transaction_codes',
            name='transaction_type',
            field=models.IntegerField(choices=[('Credit', 'Credit'), ('Debit', 'Debit')]),
        ),
    ]
