# Generated by Django 3.0.5 on 2020-05-09 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_auto_20200508_0645'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image_first',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='product',
            name='image_second',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='product',
            name='image_third',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
