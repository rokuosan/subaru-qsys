# Generated by Django 4.2.2 on 2023-07-18 14:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0012_alter_appuser_username"),
    ]

    operations = [
        migrations.AddField(
            model_name="ctfinformation",
            name="is_paused",
            field=models.BooleanField(default=False, help_text="CTF一時停止状況"),
        ),
    ]
