# Generated by Django 5.1.6 on 2025-03-19 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contact", "0003_alter_contactmodel_message_alter_contactmodel_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contactmodel",
            name="email",
            field=models.EmailField(max_length=200, unique=True),
        ),
    ]
