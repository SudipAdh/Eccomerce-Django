# Generated by Django 3.0.5 on 2020-05-11 04:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_product_size_choose'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='size_choose',
        ),
    ]
