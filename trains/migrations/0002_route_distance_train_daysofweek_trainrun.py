# Generated by Django 5.0 on 2024-01-02 17:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("trains", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="route",
            name="distance",
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name="train",
            name="daysOfWeek",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Mon", "Monday"),
                    ("Tue", "Tuesday"),
                    ("Wed", "Wednesday"),
                    ("Thu", "Thursday"),
                    ("Fri", "Friday"),
                    ("Sat", "Saturday"),
                    ("Sun", "Sunday"),
                ],
                help_text="Select the days of the week",
                max_length=20,
            ),
        ),
        migrations.CreateModel(
            name="TrainRun",
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
                ("departure_date", models.DateField()),
                ("arrival_date", models.DateField()),
                (
                    "train",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="train_runs",
                        to="trains.train",
                    ),
                ),
            ],
        ),
    ]
