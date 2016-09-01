# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voterguide', '0006_auto_20160704_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='rating',
            field=models.IntegerField(default=0, verbose_name='Rating', choices=[(100, 'Endorsed'), (60, 'Pro-Choice'), (50, 'Recommended'), (40, 'Mixed'), (20, 'Anti-Choice'), (0, 'Not Enough Information')]),
        ),
    ]
