# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voterguide', '0004_auto_20150712_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='district',
            name='state',
            field=models.CharField(default=b'MA', max_length=2, verbose_name='State'),
        ),
        migrations.AlterField(
            model_name='election',
            name='state',
            field=models.CharField(default=b'MA', max_length=2, verbose_name='State'),
        ),
        migrations.AlterField(
            model_name='race',
            name='state',
            field=models.CharField(default=b'MA', max_length=2, verbose_name='State'),
        ),
    ]
