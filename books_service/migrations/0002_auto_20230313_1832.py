# Generated by Django 4.1.7 on 2023-03-13 18:32

from django.db import migrations
from django.core.management import call_command
from django.db.migrations import RunPython


def func(apps, schema_editor):
    call_command("loaddata", "library_data.json")


class Migration(migrations.Migration):

    dependencies = [
        ("books_service", "0001_initial"),
    ]

    operations = [RunPython(func)]