# Generated by Django 2.1.2 on 2019-08-06 11:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jedzonko', '0005_auto_20190806_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 6, 13, 50, 19, 236481)),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 6, 13, 50, 19, 236497)),
        ),
    ]