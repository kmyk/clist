# Generated by Django 2.2.10 on 2020-04-16 20:05

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('true_coders', '0027_coder_date_of_birth'),
    ]

    operations = [
        migrations.AddField(
            model_name='coder',
            name='addition_fields',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict),
        ),
    ]