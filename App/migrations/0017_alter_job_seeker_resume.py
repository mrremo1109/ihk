# Generated by Django 5.1 on 2024-08-14 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0016_alter_message_sender_delete_application'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job_seeker',
            name='resume',
            field=models.FileField(default=0.0, upload_to='resumes/'),
            preserve_default=False,
        ),
    ]