# Generated by Django 3.0.5 on 2020-05-12 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_product_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='search_tags',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
