# Generated by Django 2.2 on 2020-02-07 11:33

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200207_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date_posted',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 7, 11, 33, 17, 160006, tzinfo=utc)),
        ),
    ]