# Generated by Django 3.0.7 on 2020-11-29 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobsapp', '0020_auto_20201129_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='status',
            field=models.CharField(choices=[('0', 'Undefined'), ('1', 'Selected'), ('2', 'Rejected')], default=0, max_length=30),
        ),
    ]
