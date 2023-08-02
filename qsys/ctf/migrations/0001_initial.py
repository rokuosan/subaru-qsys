# Generated by Django 4.2.3 on 2023-08-02 01:00

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_prometheus.models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
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
                    models.CharField(
                        help_text="カテゴリ名", max_length=255, unique=True
                    ),
                ),
            ],
            options={
                "verbose_name": "問題カテゴリ",
                "verbose_name_plural": "問題カテゴリ",
            },
            bases=(
                models.Model,
                django_prometheus.models.ExportModelOperationsMixin(
                    "category"
                ),
            ),
        ),
        migrations.CreateModel(
            name="CTF",
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
                    models.CharField(
                        help_text="CTF名", max_length=255, unique=True
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, default="", help_text="紹介文"),
                ),
                (
                    "start_at",
                    models.DateTimeField(
                        default=datetime.datetime(
                            2023, 8, 2, 1, 0, 30, tzinfo=datetime.timezone.utc
                        ),
                        help_text="開始日時",
                    ),
                ),
                (
                    "end_at",
                    models.DateTimeField(
                        default=datetime.datetime(
                            2023,
                            8,
                            2,
                            3,
                            0,
                            30,
                            858192,
                            tzinfo=datetime.timezone.utc,
                        ),
                        help_text="終了日時",
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
                        default=False,
                        help_text="プレイヤーランキング(Player Ranking)を公開する",
                    ),
                ),
            ],
            options={
                "verbose_name": "CTF大会情報",
                "verbose_name_plural": "CTF大会情報",
                "ordering": ["-start_at"],
            },
            bases=(
                models.Model,
                django_prometheus.models.ExportModelOperationsMixin("ctf"),
            ),
        ),
        migrations.CreateModel(
            name="Difficulty",
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
                    "level",
                    models.PositiveSmallIntegerField(
                        help_text="難易度レベル", unique=True
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="難易度名", max_length=255, unique=True
                    ),
                ),
            ],
            options={
                "verbose_name": "問題難易度",
                "verbose_name_plural": "問題難易度",
            },
            bases=(
                models.Model,
                django_prometheus.models.ExportModelOperationsMixin(
                    "difficulty"
                ),
            ),
        ),
        migrations.CreateModel(
            name="Team",
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
                    models.CharField(
                        help_text="チーム名", max_length=255, unique=True
                    ),
                ),
                (
                    "members",
                    models.ManyToManyField(
                        blank=True,
                        help_text="チームメンバー",
                        related_name="teams",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "チーム",
                "verbose_name_plural": "チーム",
            },
            bases=(
                models.Model,
                django_prometheus.models.ExportModelOperationsMixin("team"),
            ),
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text="問題ID",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "title",
                    models.CharField(help_text="問題タイトル", max_length=255),
                ),
                (
                    "description",
                    models.TextField(blank=True, default="", help_text="問題文"),
                ),
                ("flag", models.CharField(help_text="フラグ", max_length=255)),
                ("point", models.PositiveIntegerField(help_text="点数")),
                (
                    "is_open",
                    models.BooleanField(default=True, help_text="公開中かどうか"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, help_text="作成日時"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, help_text="更新日時"),
                ),
                (
                    "category",
                    models.ForeignKey(
                        default="Uncategorized",
                        help_text="カテゴリ",
                        on_delete=django.db.models.deletion.SET_DEFAULT,
                        to="ctf.category",
                    ),
                ),
                (
                    "difficulty",
                    models.ForeignKey(
                        default="Easy",
                        help_text="難易度",
                        on_delete=django.db.models.deletion.SET_DEFAULT,
                        to="ctf.difficulty",
                    ),
                ),
            ],
            options={
                "verbose_name": "問題",
                "verbose_name_plural": "問題",
            },
            bases=(
                models.Model,
                django_prometheus.models.ExportModelOperationsMixin(
                    "question"
                ),
            ),
        ),
        migrations.CreateModel(
            name="History",
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
                    "is_correct",
                    models.BooleanField(default=False, help_text="正解したかどうか"),
                ),
                (
                    "answer",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text="回答内容",
                        max_length=255,
                    ),
                ),
                (
                    "point",
                    models.PositiveIntegerField(default=0, help_text="獲得点数"),
                ),
                (
                    "result",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("correct", "正解"),
                            ("incorrect", "不正解"),
                            ("pending", "未判定"),
                            ("flag_format_error", "フラグ形式エラー"),
                            ("time_limit_exceeded", "時間切れ"),
                            ("already_answered", "回答済み"),
                        ],
                        default="",
                        help_text="判定結果",
                        max_length=255,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, help_text="回答日時"),
                ),
                (
                    "question",
                    models.ForeignKey(
                        help_text="問題",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ctf.question",
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        help_text="チーム",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ctf.team",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        help_text="回答者",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "回答履歴",
                "verbose_name_plural": "回答履歴",
            },
            bases=(
                models.Model,
                django_prometheus.models.ExportModelOperationsMixin("history"),
            ),
        ),
    ]
