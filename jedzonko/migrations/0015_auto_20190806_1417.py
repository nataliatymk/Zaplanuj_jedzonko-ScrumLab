# Generated by Django 2.1.2 on 2019-08-06 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jedzonko', '0014_auto_20190806_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
