# Generated by Django 2.1.7 on 2019-08-18 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('true_coders', '0019_filter_arr_categories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filter',
            name='categories',
        ),
    ]
