# Generated by Django 3.0.6 on 2020-05-24 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20200524_0607'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shopcart',
            old_name='quatity',
            new_name='quantity',
        ),
    ]