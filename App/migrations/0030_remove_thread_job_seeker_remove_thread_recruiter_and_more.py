# Generated by Django 5.1 on 2024-08-22 00:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0029_alter_thread_unique_together_thread_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thread',
            name='job_seeker',
        ),
        migrations.RemoveField(
            model_name='thread',
            name='recruiter',
        ),
        migrations.DeleteModel(
            name='ChatMessage',
        ),
        migrations.DeleteModel(
            name='Thread',
        ),
    ]
