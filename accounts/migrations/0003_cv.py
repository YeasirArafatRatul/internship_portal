# Generated by Django 3.0.7 on 2020-10-29 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20190326_1754'),
    ]

    operations = [
        migrations.CreateModel(
            name='CV',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='')),
                ('description', models.TextField()),
                ('updated', models.DateField(auto_now=True)),
                ('created', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
