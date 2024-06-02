# Generated by Django 5.0.6 on 2024-05-18 04:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0005_player_max_single_games_player_min_double_games_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="match",
            name="opposing_team",
        ),
        migrations.AddField(
            model_name="team",
            name="match",
            field=models.OneToOneField(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="teams.match",
            ),
            preserve_default=False,
        ),
    ]
