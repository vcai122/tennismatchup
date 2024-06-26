# Generated by Django 5.0.6 on 2024-05-18 04:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0006_remove_match_opposing_team_team_match"),
    ]

    operations = [
        migrations.CreateModel(
            name="Assignment",
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
                    "doubles_one_first",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="doubles_one_first",
                        to="teams.player",
                    ),
                ),
                (
                    "doubles_one_second",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="doubles_one_second",
                        to="teams.player",
                    ),
                ),
                (
                    "doubles_three_first",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="doubles_three_first",
                        to="teams.player",
                    ),
                ),
                (
                    "doubles_three_second",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="doubles_three_second",
                        to="teams.player",
                    ),
                ),
                (
                    "doubles_two_first",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="doubles_two_first",
                        to="teams.player",
                    ),
                ),
                (
                    "doubles_two_second",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="doubles_two_second",
                        to="teams.player",
                    ),
                ),
                (
                    "match",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="teams.match"
                    ),
                ),
                (
                    "singles_one",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="singles_one",
                        to="teams.player",
                    ),
                ),
                (
                    "singles_two",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="singles_two",
                        to="teams.player",
                    ),
                ),
            ],
        ),
    ]
