# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voterguide', '0002_auto_20150629_0001'),
    ]

    operations = [
        migrations.AddField(
            model_name='district',
            name='city',
            field=models.CharField(max_length=100, null=True, verbose_name='City', blank=True),
        ),
    ]
