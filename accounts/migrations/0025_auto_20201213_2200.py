# Generated by Django 3.0.7 on 2020-12-13 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_auto_20201213_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='passing_year',
            field=models.DateTimeField(),
        ),
    ]
