# Generated by Django 4.2.2 on 2023-07-07 12:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0004_ctfscore_team"),
    ]

    operations = [
        migrations.AddField(
            model_name="ctfinformation",
            name="questions",
            field=models.ManyToManyField(
                blank=True, help_text="問題", to="app.ctfquestion"
            ),
        ),
    ]