# Generated by Django 3.0.7 on 2020-12-13 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobsapp', '0026_auto_20201213_2201'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='last_date',
            new_name='last_date_of_app',
        ),
    ]