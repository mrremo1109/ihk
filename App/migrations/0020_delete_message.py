# Generated by Django 5.1 on 2024-08-20 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0019_message_delete_chatmessage'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Message',
        ),
    ]