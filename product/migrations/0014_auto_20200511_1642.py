# Generated by Django 3.0.6 on 2020-05-12 00:42

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='detail',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]