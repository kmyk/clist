# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-06 03:16


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0020_auto_20180206_0221'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='is_coach',
            field=models.BooleanField(default=False),
        ),
    ]
