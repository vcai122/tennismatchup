# Generated by Django 5.0.6 on 2024-05-18 06:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0010_pair"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Pair",
        ),
    ]