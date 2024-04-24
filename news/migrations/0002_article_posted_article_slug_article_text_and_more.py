# Generated by Django 4.1 on 2024-04-08 02:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("news", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="posted",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="article",
            name="slug",
            field=models.TextField(default=2019, verbose_name=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="article",
            name="text",
            field=models.TextField(default=2019),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="article",
            name="timestamp",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]