# Generated by Django 2.2 on 2019-11-10 17:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='content_published',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 10, 12, 18, 31, 567294), verbose_name='date published'),
        ),
    ]