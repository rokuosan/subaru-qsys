# Generated by Django 4.2.2 on 2023-07-12 11:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0010_ctfanswerhistory_ctf"),
    ]

    operations = [
        migrations.AddField(
            model_name="ctfinformation",
            name="show_player_ranking",
            field=models.BooleanField(
                default=True, help_text="プレイヤーランキング(Player Ranking)を公開する"
            ),
        ),
        migrations.AddField(
            model_name="ctfinformation",
            name="show_team_ranking",
            field=models.BooleanField(
                default=True, help_text="チームランキング(Team Ranking)を公開する"
            ),
        ),
    ]