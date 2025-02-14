# Generated by Django 5.0.6 on 2024-07-17 09:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_remove_bonus_tran_statust_alter_myuser_my_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='keyBonus',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='my_status',
            field=models.CharField(blank=True, choices=[('inactive', 'inactive'), ('renewal', 'incomplete'), ('active', 'renewal'), ('incomplete', 'active')], default='incomplete', max_length=255, null=True),
        ),
    ]
