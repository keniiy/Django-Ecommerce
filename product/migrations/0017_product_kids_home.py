# Generated by Django 3.0.6 on 2020-05-15 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0016_auto_20200515_1132'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='kids_home',
            field=models.BooleanField(default=True),
        ),
    ]
