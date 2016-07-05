# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voterguide', '0005_auto_20160628_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='district',
            name='chamber',
            field=models.IntegerField(verbose_name='Chamber', choices=[(1, 'State Senate'), (2, 'State House'), (3, 'County'), (4, 'City Council'), (5, 'US Senate'), (6, 'US House')]),
        ),
        migrations.AlterField(
            model_name='office',
            name='chamber',
            field=models.IntegerField(blank=True, help_text='Optional', null=True, verbose_name='Chamber', choices=[(1, 'State Senate'), (2, 'State House'), (3, 'County'), (4, 'City Council'), (5, 'US Senate'), (6, 'US House')]),
        ),
    ]
