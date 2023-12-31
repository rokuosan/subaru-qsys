# Generated by Django 4.2.3 on 2023-08-02 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("ctf", "0018_contest_is_open"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="category",
            field=models.ForeignKey(
                help_text="カテゴリ",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="questions",
                to="ctf.category",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="difficulty",
            field=models.ForeignKey(
                help_text="難易度",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="questions",
                to="ctf.difficulty",
            ),
        ),
    ]
