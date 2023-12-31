# Generated by Django 4.2.3 on 2023-08-02 01:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ctf", "0002_alter_ctf_end_at_alter_ctf_start_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ctf",
            name="end_at",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 8, 2, 3, 1, 48, 733675, tzinfo=datetime.timezone.utc
                ),
                help_text="終了日時",
            ),
        ),
        migrations.AlterField(
            model_name="ctf",
            name="start_at",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 8, 2, 1, 1, 48, tzinfo=datetime.timezone.utc
                ),
                help_text="開始日時",
            ),
        ),
    ]
