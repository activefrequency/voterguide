# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voterguide', '0010_auto_20170713_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='party',
            field=models.CharField(blank=True, max_length=2, null=True, verbose_name='Party', choices=[('D', 'Democrat'), ('R', 'Republican'), ('I', 'Independent'), ('L', 'Libertarian'), ('SO', 'Socialist'), ('DS', 'Democratic Socialist'), ('PP', "People's Party"), ('G', 'Green'), ('U', 'United Ind.'), ('N', 'Unaffiliated')]),
        ),
        migrations.AlterField(
            model_name='district',
            name='chamber',
            field=models.IntegerField(verbose_name='Chamber', choices=[(1, 'State Senate'), (2, 'State House'), (3, 'County'), (8, 'Mayor'), (4, 'City Council'), (9, 'City Attorney'), (10, 'School Board'), (5, 'US Senate'), (6, 'US House'), (7, "Governor's Council")]),
        ),
        migrations.AlterField(
            model_name='office',
            name='chamber',
            field=models.IntegerField(blank=True, help_text='Optional', null=True, verbose_name='Chamber', choices=[(1, 'State Senate'), (2, 'State House'), (3, 'County'), (8, 'Mayor'), (4, 'City Council'), (9, 'City Attorney'), (10, 'School Board'), (5, 'US Senate'), (6, 'US House'), (7, "Governor's Council")]),
        ),
    ]
