# Generated by Django 4.2.10 on 2025-04-24 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("activities", "0004_alter_activitiesmodel_content_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="activitiesmodel",
            name="description",
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name="activitiesmodel",
            name="keywords",
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name="activitiesmodel",
            name="slug",
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
