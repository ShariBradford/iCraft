# Generated by Django 2.2 on 2020-08-10 20:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0007_auto_20200809_2143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='address',
        ),
        migrations.RemoveField(
            model_name='user',
            name='areas_of_interest',
        ),
        migrations.RemoveField(
            model_name='user',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='user',
            name='city',
        ),
        migrations.RemoveField(
            model_name='user',
            name='company',
        ),
        migrations.RemoveField(
            model_name='user',
            name='state',
        ),
    ]
