# Generated by Django 5.0.1 on 2024-08-14 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0013_recruiter_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recruiter',
            name='location',
        ),
    ]