# Generated by Django 5.0 on 2024-01-02 14:05

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("stations", "0001_initial"),
        ("trains", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Passenger",
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
                ("name", models.CharField(max_length=100)),
                ("age", models.PositiveSmallIntegerField()),
                (
                    "gender",
                    models.CharField(
                        choices=[("M", "Male"), ("F", "Female")], max_length=1
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Ticket",
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
                ("booking_time", models.DateTimeField(auto_now_add=True)),
                (
                    "unique_id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                (
                    "departure_station",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="departure_tickets",
                        to="stations.station",
                    ),
                ),
                (
                    "destination_station",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="destination_tickets",
                        to="stations.station",
                    ),
                ),
                (
                    "passenger",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tickets.passenger",
                    ),
                ),
                (
                    "train",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="trains.train"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
