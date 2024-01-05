# Generated by Django 5.0 on 2024-01-05 02:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tickets", "0004_alter_ticket_passenger"),
    ]

    operations = [
        migrations.AlterField(
            model_name="passenger",
            name="ticket",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="passengers",
                to="tickets.ticket",
            ),
        ),
    ]
