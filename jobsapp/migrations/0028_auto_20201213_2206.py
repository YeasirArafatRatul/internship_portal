# Generated by Django 3.0.7 on 2020-12-13 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobsapp', '0027_auto_20201213_2205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='last_date_of_app',
        ),
        migrations.AddField(
            model_name='job',
            name='last_time',
            field=models.DateField(blank=True, null=True),
        ),
    ]