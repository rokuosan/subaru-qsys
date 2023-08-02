# Generated by Django 4.2.2 on 2023-08-02 08:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("ctf", "0016_remove_difficulty_level"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="category",
            field=models.ForeignKey(
                help_text="カテゴリ",
                on_delete=django.db.models.deletion.CASCADE,
                to="ctf.category",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="difficulty",
            field=models.ForeignKey(
                help_text="難易度",
                on_delete=django.db.models.deletion.CASCADE,
                to="ctf.difficulty",
            ),
        ),
    ]