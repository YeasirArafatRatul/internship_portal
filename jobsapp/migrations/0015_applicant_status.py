# Generated by Django 3.0.7 on 2020-11-15 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobsapp', '0014_auto_20201105_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicant',
            name='status',
            field=models.CharField(blank=True, choices=[('1', 'Received'), ('2', 'Selected'), ('3', 'Rejected')], max_length=30, null=True),
        ),
    ]
