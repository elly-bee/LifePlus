# Generated by Django 5.0.6 on 2024-07-13 20:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_transaction_ccctype_alter_account_amount_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='cccType',
            new_name='accType',
        ),
    ]
