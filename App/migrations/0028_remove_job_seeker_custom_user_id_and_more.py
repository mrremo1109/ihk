# Generated by Django 5.1 on 2024-08-21 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0027_job_seeker_custom_user_id_recruiter_custom_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job_seeker',
            name='custom_user_id',
        ),
        migrations.RemoveField(
            model_name='recruiter',
            name='custom_user_id',
        ),
    ]