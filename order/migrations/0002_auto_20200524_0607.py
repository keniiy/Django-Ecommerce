# Generated by Django 3.0.6 on 2020-05-24 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shopcart',
            old_name='Product',
            new_name='product',
        ),
    ]
