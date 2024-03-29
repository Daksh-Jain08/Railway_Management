# Generated by Django 5.0 on 2024-01-16 04:24

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Station",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("stationName", models.CharField(max_length=100)),
                ("stationCode", models.CharField(max_length=5, unique=True)),
            ],
        ),
    ]
