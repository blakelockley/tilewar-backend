# Generated by Django 3.1.7 on 2024-07-30 05:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("players", "0002_team_number"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="team",
            options={"ordering": ("number",)},
        ),
    ]
