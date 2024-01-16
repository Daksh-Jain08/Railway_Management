# Generated by Django 5.0 on 2024-01-16 19:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("trains", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SeatClass",
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
                (
                    "seat_class",
                    models.TextField(
                        choices=[
                            ("3A", "Third AC"),
                            ("2A", "Second AC"),
                            ("1A", "First AC"),
                            ("S", "Sleeper"),
                        ],
                        default="S",
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="train",
            name="baseFare",
        ),
        migrations.RemoveField(
            model_name="train",
            name="numberOfSeats",
        ),
        migrations.RemoveField(
            model_name="trainrun",
            name="numberOfAvailableSeats",
        ),
        migrations.AddField(
            model_name="train",
            name="baseFare1AC",
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name="train",
            name="baseFare2AC",
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name="train",
            name="baseFare3AC",
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name="train",
            name="baseFareSleeper",
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name="train",
            name="numberOf1AC",
            field=models.IntegerField(
                null=True, validators=[django.core.validators.MinValueValidator(0)]
            ),
        ),
        migrations.AddField(
            model_name="train",
            name="numberOf2AC",
            field=models.IntegerField(
                null=True, validators=[django.core.validators.MinValueValidator(0)]
            ),
        ),
        migrations.AddField(
            model_name="train",
            name="numberOf3AC",
            field=models.IntegerField(
                null=True, validators=[django.core.validators.MinValueValidator(0)]
            ),
        ),
        migrations.AddField(
            model_name="train",
            name="numberOfSleeper",
            field=models.IntegerField(
                null=True, validators=[django.core.validators.MinValueValidator(0)]
            ),
        ),
        migrations.AddField(
            model_name="trainrun",
            name="numberOfAvailable1AC",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="trainrun",
            name="numberOfAvailable2AC",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="trainrun",
            name="numberOfAvailable3AC",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="trainrun",
            name="numberOfAvailableSleeper",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="train",
            name="totalDistance",
            field=models.PositiveIntegerField(),
        ),
    ]
