# Generated by Django 3.0.6 on 2020-05-10 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_auto_20200510_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(to='product.Category'),
        ),
    ]
