# Generated by Django 2.2 on 2020-08-15 21:53

import classes.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0009_auto_20200815_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='/media/blank-user.jpg', null=True, upload_to=classes.models.user_directory_path),
        ),
    ]
