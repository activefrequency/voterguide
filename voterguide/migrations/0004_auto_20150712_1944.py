# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voterguide', '0003_auto_20150710_1904'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='district',
            options={'ordering': ['chamber', 'code', 'name', 'idx'], 'verbose_name': 'District', 'verbose_name_plural': 'Districts'},
        ),
        migrations.AddField(
            model_name='candidate',
            name='about_blurb',
            field=models.TextField(help_text='Candidate Statement (can contain HTML)', max_length=500, verbose_name="'About' Blurb", blank=True),
        ),
    ]
