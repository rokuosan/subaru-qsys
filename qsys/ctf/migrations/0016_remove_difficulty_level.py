# Generated by Django 4.2.2 on 2023-08-02 08:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("ctf", "0015_contest_questions"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="difficulty",
            name="level",
        ),
    ]
