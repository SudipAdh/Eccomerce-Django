# Generated by Django 3.0.5 on 2020-05-11 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_auto_20200509_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='size_choose',
            field=models.CharField(choices=[(1, 'small'), (2, 'medium'), (3, 'large'), (4, 'extra large')], default=1, max_length=1),
        ),
    ]
