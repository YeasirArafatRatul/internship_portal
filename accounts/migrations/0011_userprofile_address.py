# Generated by Django 3.0.7 on 2020-11-10 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_education_degree'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='address',
            field=models.CharField(default='Write Your Adress Here', max_length=300),
        ),
    ]