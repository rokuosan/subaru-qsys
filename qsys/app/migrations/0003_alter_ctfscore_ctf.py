# Generated by Django 4.2.2 on 2023-07-07 09:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0002_ctfanswerhistory_team_alter_appuser_username"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ctfscore",
            name="ctf",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="app.ctfinformation",
            ),
        ),
    ]
