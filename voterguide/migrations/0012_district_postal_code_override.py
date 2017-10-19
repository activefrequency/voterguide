# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voterguide', '0011_auto_20171018_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='district',
            name='postal_code_override',
            field=models.CharField(help_text="If the address is in one of these postal codes, assume it's in this district (used for fixing Google Maps geocoding errors).", max_length=100, null=True, verbose_name='ZIP codes', blank=True),
        ),
    ]
