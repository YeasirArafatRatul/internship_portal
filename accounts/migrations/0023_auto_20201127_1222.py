# Generated by Django 3.0.7 on 2020-11-27 06:22

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_course_institute_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='benefits',
            name='details',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
