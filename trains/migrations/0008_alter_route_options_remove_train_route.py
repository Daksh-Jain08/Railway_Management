# Generated by Django 5.0 on 2024-01-08 18:02

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("trains", "0007_train_route"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="route",
            options={"ordering": ["order"]},
        ),
        migrations.RemoveField(
            model_name="train",
            name="route",
        ),
    ]