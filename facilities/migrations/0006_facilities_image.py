# Generated by Django 4.2.10 on 2025-04-27 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("facilities", "0005_alter_facilities_content_alter_facilities_heading"),
    ]

    operations = [
        migrations.AddField(
            model_name="facilities",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="images/"),
        ),
    ]
