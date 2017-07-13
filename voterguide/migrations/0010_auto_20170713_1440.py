# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voterguide', '0009_auto_20170709_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='party',
            field=models.CharField(blank=True, max_length=2, null=True, verbose_name='Party', choices=[('D', 'Democrat'), ('R', 'Republican'), ('I', 'Independent'), ('L', 'Libertarian'), ('SO', 'Socialist'), ('DS', 'Democratic Socialist'), ('G', 'Green'), ('U', 'United Ind.'), ('N', 'Unaffiliated')]),
        ),
    ]
