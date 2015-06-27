# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_incumbent', models.BooleanField(default=False, verbose_name='Incumbent')),
                ('party', models.CharField(blank=True, max_length=2, null=True, verbose_name='Party', choices=[('D', 'Democrat'), ('R', 'Republican'), ('I', 'Independent'), ('L', 'Libertarian'), ('G', 'Green'), ('U', 'United Ind.'), ('N', 'Unaffiliated')])),
                ('rating', models.IntegerField(default=0, verbose_name='Rating', choices=[(100, 'Endorsed'), (60, 'Pro-Choice'), (50, 'Recommended'), (40, 'Mixed'), (20, 'Anti-Choice'), (0, 'Unknown')])),
                ('featured', models.BooleanField(default=False, verbose_name='Featured')),
                ('winner', models.BooleanField(default=False, verbose_name='Winner')),
                ('is_endorsed', models.BooleanField(default=False, verbose_name='Endorsed?', editable=False)),
                ('is_pro', models.BooleanField(default=False, verbose_name='Endorsed or Pro?', editable=False)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('modified_on', models.DateTimeField(auto_now=True, verbose_name='Modified')),
            ],
            options={
                'ordering': ['race__state', 'race__election', 'race__office', 'race__district', 'person__last_name', 'person__first_name'],
                'verbose_name': 'Candidate',
                'verbose_name_plural': 'Candidates',
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('code', models.CharField(help_text="Sortable code, i.e. 'MID08'", max_length=50, verbose_name='Code', blank=True)),
                ('idx', models.IntegerField(default=0, help_text="Sort order; useful if sorting by district name alphabetically doesn't make sense and we don't have codes. ", verbose_name='Order')),
                ('state', models.CharField(default=b'WA', max_length=2, verbose_name='State')),
                ('chamber', models.IntegerField(verbose_name='Chamber', choices=[(1, 'State Senate'), (2, 'State House'), (3, 'County')])),
                ('num_seats', models.IntegerField(default=1, help_text='Number of seats in district - typically 1', verbose_name='# Seats')),
                ('openstates_id', models.CharField(help_text="ID from OpenStates API, e.g. 'ma-lower-Eighth Middlesex'", max_length=100, null=True, verbose_name='OpenStates ID', blank=True)),
                ('openstates_boundary_id', models.CharField(help_text="Boundary ID from OpenStates API, e.g. 'sldu/ma-worcester-middlesex'", max_length=100, null=True, verbose_name='OpenStates Boundary ID', blank=True)),
                ('boundaries', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, verbose_name='Boundaries', blank=True)),
                ('county', models.CharField(max_length=100, null=True, verbose_name='County', blank=True)),
                ('is_floterial', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('modified_on', models.DateTimeField(auto_now=True, verbose_name='Modified')),
                ('floterial_to', models.ManyToManyField(related_name='floterial_to_rel_+', to='voterguide.District', blank=True)),
            ],
            options={
                'ordering': ['chamber', 'idx', 'code', 'name'],
                'verbose_name': 'District',
                'verbose_name_plural': 'Districts',
            },
        ),
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('state', models.CharField(default=b'WA', max_length=2, verbose_name='State')),
                ('year', models.IntegerField(default=b'2014', verbose_name='Year')),
                ('election_type', models.CharField(max_length=1, verbose_name='Election type', choices=[('P', 'Primary'), ('G', 'General'), ('S', 'Special')])),
                ('election_date', models.DateField(verbose_name='Election date')),
                ('is_active', models.BooleanField(help_text="Only one election at a time should be 'active' - this is what's featured on the site.", verbose_name='Active')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('modified_on', models.DateTimeField(auto_now=True, verbose_name='Modified')),
            ],
            options={
                'ordering': ['-is_active', 'election_date'],
                'verbose_name': 'Election',
                'verbose_name_plural': 'Elections',
            },
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('priority', models.IntegerField(default=0, help_text="Higher score means it'll be listed first in a list with multiple offices.", verbose_name='Priority')),
                ('chamber', models.IntegerField(blank=True, help_text='Optional', null=True, verbose_name='Chamber', choices=[(1, 'State Senate'), (2, 'State House'), (3, 'County')])),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('modified_on', models.DateTimeField(auto_now=True, verbose_name='Modified')),
            ],
            options={
                'ordering': ['-priority'],
                'verbose_name': 'Office',
                'verbose_name_plural': 'Offices',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('full_name', models.CharField(help_text='How the full name should be displayed, with any punctuation.', max_length=100, verbose_name='Full name', blank=True)),
                ('first_name', models.CharField(max_length=50, verbose_name='First name', blank=True)),
                ('middle', models.CharField(max_length=50, verbose_name='Middle name', blank=True)),
                ('last_name', models.CharField(max_length=50, verbose_name='Last name', blank=True)),
                ('suffixes', models.CharField(max_length=50, verbose_name='Suffixes', blank=True)),
                ('openstates_legid', models.CharField(help_text="Permanent OpenStates leg_id - i.e. 'ILL000555'", max_length=20, verbose_name='OpenStates ID', blank=True)),
                ('photo_url', models.CharField(help_text='URL to candidate photo (optional)', max_length=200, verbose_name='Photo URL', blank=True)),
                ('blurb', models.TextField(help_text='Blurb if featured (can contain HTML)', max_length=500, verbose_name='Blurb', blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('modified_on', models.DateTimeField(auto_now=True, verbose_name='Modified')),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
                'verbose_name': 'Person',
                'verbose_name_plural': 'People',
            },
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(default=b'WA', max_length=2, verbose_name='State')),
                ('has_endorsement', models.BooleanField(default=False, editable=False)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('modified_on', models.DateTimeField(auto_now=True, verbose_name='Modified')),
                ('district', models.ForeignKey(blank=True, to='voterguide.District', help_text='Optional - blank if statewide race.', null=True)),
                ('election', models.ForeignKey(to='voterguide.Election')),
                ('office', models.ForeignKey(to='voterguide.Office')),
            ],
            options={
                'ordering': ['state', 'election', 'office', 'district'],
                'verbose_name': 'Race',
                'verbose_name_plural': 'Races',
            },
        ),
        migrations.AddField(
            model_name='candidate',
            name='person',
            field=models.ForeignKey(to='voterguide.Person'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='race',
            field=models.ForeignKey(to='voterguide.Race'),
        ),
    ]
