# Generated by Django 5.1 on 2024-08-10 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0010_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='appliedpost',
            name='status',
            field=models.CharField(choices=[('reviewing', 'Reviewing'), ('selected', 'Selected'), ('rejected', 'Rejected')], default='reviewing', max_length=20),
        ),
        migrations.AddField(
            model_name='job_seeker',
            name='address',
            field=models.TextField(blank=True, max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='job_seeker',
            name='resume',
            field=models.FileField(blank=True, null=True, upload_to='resumes/'),
        ),
        migrations.AddField(
            model_name='recruiter',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
    ]
