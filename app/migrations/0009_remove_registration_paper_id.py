# Generated by Django 5.1 on 2024-10-02 08:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0008_alter_registration_paper_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="registration",
            name="paper_id",
        ),
    ]
