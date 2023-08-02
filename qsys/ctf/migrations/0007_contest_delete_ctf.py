# Generated by Django 4.2.3 on 2023-08-02 02:42

from django.db import migrations, models
import django.utils.timezone
import django_prometheus.models


class Migration(migrations.Migration):
    dependencies = [
        ("ctf", "0006_remove_history_user_alter_ctf_end_at_player_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Contest",
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
                    "name",
                    models.CharField(help_text="コンテスト名", max_length=255, unique=True),
                ),
                (
                    "description",
                    models.TextField(blank=True, default="", help_text="紹介文"),
                ),
                (
                    "start_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, help_text="開始日時"
                    ),
                ),
                (
                    "end_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, help_text="終了日時"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("preparing", "準備中"),
                            ("running", "開催中"),
                            ("paused", "一時停止中"),
                            ("finished", "終了"),
                        ],
                        default="preparing",
                        help_text="CTFの状態",
                        max_length=255,
                    ),
                ),
                (
                    "is_team_ranking_public",
                    models.BooleanField(
                        default=True, help_text="チームランキング(Team Ranking)を公開する"
                    ),
                ),
                (
                    "is_player_ranking_public",
                    models.BooleanField(
                        default=False, help_text="プレイヤーランキング(Player Ranking)を公開する"
                    ),
                ),
            ],
            options={
                "verbose_name": "コンテスト大会情報",
                "verbose_name_plural": "コンテスト大会情報",
                "ordering": ["-start_at"],
            },
            bases=(
                models.Model,
                django_prometheus.models.ExportModelOperationsMixin("ctf"),
            ),
        ),
        migrations.DeleteModel(
            name="CTF",
        ),
    ]