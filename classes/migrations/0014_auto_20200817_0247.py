# Generated by Django 2.2 on 2020-08-17 06:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0013_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='rating',
            name='number_of_stars',
            field=models.PositiveSmallIntegerField(choices=[(1, 'It was awful!'), (2, 'Not so great.'), (3, 'Just Ok.'), (4, 'I liked it!'), (5, 'Pretty freakin awesome!')], validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
