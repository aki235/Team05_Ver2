# Generated by Django 5.0.6 on 2024-06-14 22:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="user_point",
            field=models.IntegerField(default=5),
        ),
    ]
