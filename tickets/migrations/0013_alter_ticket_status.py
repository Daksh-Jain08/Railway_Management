# Generated by Django 5.0 on 2024-01-08 09:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tickets", "0012_alter_ticket_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticket",
            name="status",
            field=models.CharField(max_length=10, null=True),
        ),
    ]
