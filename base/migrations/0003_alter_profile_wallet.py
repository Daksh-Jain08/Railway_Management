# Generated by Django 5.0 on 2024-01-14 01:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0002_alter_profile_tickets"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="wallet",
            field=models.FloatField(default=0),
        ),
    ]