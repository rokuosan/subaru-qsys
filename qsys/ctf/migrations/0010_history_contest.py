# Generated by Django 4.2.3 on 2023-08-02 03:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("ctf", "0009_alter_contest_display_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="history",
            name="contest",
            field=models.ForeignKey(
                default=0,
                help_text="CTFコンテスト",
                on_delete=django.db.models.deletion.CASCADE,
                to="ctf.contest",
            ),
            preserve_default=False,
        ),
    ]
