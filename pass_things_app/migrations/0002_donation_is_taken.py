# Generated by Django 2.2.19 on 2021-03-11 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pass_things_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='is_taken',
            field=models.BooleanField(default=None, null=True),
        ),
    ]