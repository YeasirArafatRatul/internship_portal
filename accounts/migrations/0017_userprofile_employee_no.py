# Generated by Django 3.0.7 on 2020-11-27 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20201125_2325'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='employee_no',
            field=models.PositiveIntegerField(default=1),
        ),
    ]