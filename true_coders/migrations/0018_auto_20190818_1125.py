# Generated by Django 2.1.7 on 2019-08-18 11:25

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('true_coders', '0017_party_is_hidden'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coder',
            name='settings',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='filter',
            name='categories',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=['list', 'calendar', 'email', 'telegram', 'api']),
        ),
        migrations.AlterField(
            model_name='filter',
            name='resources',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list),
        ),
    ]
