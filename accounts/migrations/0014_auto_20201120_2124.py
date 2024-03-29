# Generated by Django 3.0.7 on 2020-11-20 15:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_comapanyimages'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComapanyImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_image', models.ImageField(blank=True, default='avatar.png', null=True, upload_to='company_images')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.User')),
            ],
        ),
        migrations.DeleteModel(
            name='ComapanyImages',
        ),
    ]
