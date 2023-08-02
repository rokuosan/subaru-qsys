# Generated by Django 4.2.3 on 2023-08-02 03:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ctf", "0007_contest_delete_ctf"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="contest",
            options={
                "ordering": ["-start_at"],
                "verbose_name": "コンテスト",
                "verbose_name_plural": "コンテスト",
            },
        ),
        migrations.RemoveField(
            model_name="contest",
            name="name",
        ),
        migrations.AddField(
            model_name="contest",
            name="display_name",
            field=models.CharField(help_text="コンテスト名", max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="contest",
            name="id",
            field=models.CharField(
                help_text="コンテストID",
                max_length=255,
                primary_key=True,
                serialize=False,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="IDは半角英数字とハイフン(-)、アンダースコア(_)のみ使用でき、4文字以上である必要があります。",
                        regex="^[a-zA-Z0-9_-]{4,}$",
                    )
                ],
            ),
        ),
    ]