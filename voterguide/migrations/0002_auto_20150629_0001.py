# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voterguide', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='district',
            name='chamber',
            field=models.IntegerField(verbose_name='Chamber', choices=[(1, 'State Senate'), (2, 'State House'), (3, 'County'), (4, 'City Council')]),
        ),
        migrations.AlterField(
            model_name='office',
            name='chamber',
            field=models.IntegerField(blank=True, help_text='Optional', null=True, verbose_name='Chamber', choices=[(1, 'State Senate'), (2, 'State House'), (3, 'County'), (4, 'City Council')]),
        ),
    ]
