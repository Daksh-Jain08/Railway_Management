# Generated by Django 5.0 on 2024-01-09 07:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("trains", "0012_alter_day_day"),
    ]

    operations = [
        migrations.AddField(
            model_name="train",
            name="daysOfJourney",
            field=models.IntegerField(null=True),
        ),
    ]