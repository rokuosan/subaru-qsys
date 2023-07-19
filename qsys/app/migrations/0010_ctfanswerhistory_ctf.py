# Generated by Django 4.2.2 on 2023-07-09 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0009_ctfinformation_participants"),
    ]

    operations = [
        migrations.AddField(
            model_name="ctfanswerhistory",
            name="ctf",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="answer_history",
                to="app.ctfinformation",
            ),
        ),
    ]
