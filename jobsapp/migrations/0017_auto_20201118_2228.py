# Generated by Django 3.0.7 on 2020-11-18 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobsapp', '0016_auto_20201115_2354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='type',
            field=models.CharField(choices=[('paid', 'Paid'), ('unpaid', 'Unpaid')], max_length=10),
        ),
    ]
