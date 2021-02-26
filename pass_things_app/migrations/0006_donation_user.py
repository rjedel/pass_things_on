# Generated by Django 2.2.19 on 2021-02-26 16:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pass_things_app', '0005_remove_donation_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='donations', to=settings.AUTH_USER_MODEL),
        ),
    ]
