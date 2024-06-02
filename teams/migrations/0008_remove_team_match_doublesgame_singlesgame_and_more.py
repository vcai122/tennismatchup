# Generated by Django 5.0.6 on 2024-05-18 04:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0007_assignment"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="team",
            name="match",
        ),
        migrations.CreateModel(
            name="DoublesGame",
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
                ("opponent_score", models.IntegerField(default=6)),
                (
                    "match",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="teams.match"
                    ),
                ),
                (
                    "player_one",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="player_one",
                        to="teams.player",
                    ),
                ),
                (
                    "player_two",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="player_two",
                        to="teams.player",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SinglesGame",
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
                ("opponent_score", models.IntegerField(default=6)),
                (
                    "match",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="teams.match"
                    ),
                ),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="teams.player"
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="Assignment",
        ),
        migrations.DeleteModel(
            name="Team",
        ),
    ]
