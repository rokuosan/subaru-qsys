# Generated by Django 4.2.3 on 2023-08-02 07:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ctf", "0014_contest_teams_alter_player_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="contest",
            name="questions",
            field=models.ManyToManyField(
                blank=True,
                help_text="問題",
                related_name="contests",
                to="ctf.question",
            ),
        ),
    ]
