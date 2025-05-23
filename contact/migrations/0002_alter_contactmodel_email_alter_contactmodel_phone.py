# Generated by Django 5.1.6 on 2025-02-27 10:07

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contact", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contactmodel",
            name="email",
            field=models.EmailField(max_length=320, unique=True),
        ),
        migrations.AlterField(
            model_name="contactmodel",
            name="phone",
            field=phonenumber_field.modelfields.PhoneNumberField(
                max_length=128, region=None
            ),
        ),
    ]
