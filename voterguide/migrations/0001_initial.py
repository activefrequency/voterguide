# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Election'
        db.create_table(u'voterguide_election', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('state', self.gf('django.db.models.fields.CharField')(default='MA', max_length=2)),
            ('year', self.gf('django.db.models.fields.IntegerField')(default='2014')),
            ('election_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('election_date', self.gf('django.db.models.fields.DateField')()),
            ('is_active', self.gf('django.db.models.fields.BooleanField')()),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'voterguide', ['Election'])

        # Adding model 'District'
        db.create_table(u'voterguide_district', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('idx', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('state', self.gf('django.db.models.fields.CharField')(default='MA', max_length=2)),
            ('chamber', self.gf('django.db.models.fields.IntegerField')()),
            ('num_seats', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('openstates_id', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('openstates_boundary_id', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('boundaries', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(null=True, blank=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'voterguide', ['District'])

        # Adding model 'Office'
        db.create_table(u'voterguide_office', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('priority', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('chamber', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'voterguide', ['Office'])

        # Adding model 'Race'
        db.create_table(u'voterguide_race', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('election', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voterguide.Election'])),
            ('office', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voterguide.Office'])),
            ('state', self.gf('django.db.models.fields.CharField')(default='MA', max_length=2)),
            ('district', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voterguide.District'], null=True, blank=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'voterguide', ['Race'])

        # Adding model 'Person'
        db.create_table(u'voterguide_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('middle', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('suffixes', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('openstates_legid', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('photo_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'voterguide', ['Person'])

        # Adding model 'Candidate'
        db.create_table(u'voterguide_candidate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voterguide.Person'])),
            ('race', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voterguide.Race'])),
            ('is_incumbent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('party', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('rating', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'voterguide', ['Candidate'])


    def backwards(self, orm):
        # Deleting model 'Election'
        db.delete_table(u'voterguide_election')

        # Deleting model 'District'
        db.delete_table(u'voterguide_district')

        # Deleting model 'Office'
        db.delete_table(u'voterguide_office')

        # Deleting model 'Race'
        db.delete_table(u'voterguide_race')

        # Deleting model 'Person'
        db.delete_table(u'voterguide_person')

        # Deleting model 'Candidate'
        db.delete_table(u'voterguide_candidate')


    models = {
        u'voterguide.candidate': {
            'Meta': {'ordering': "[u'race__state', u'race__election', u'race__office', u'race__district', u'person__last_name', u'person__first_name']", 'object_name': 'Candidate'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_incumbent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'party': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voterguide.Person']"}),
            'race': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voterguide.Race']"}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'voterguide.district': {
            'Meta': {'ordering': "[u'-chamber', u'idx', u'code', u'name']", 'object_name': 'District'},
            'boundaries': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True', 'blank': 'True'}),
            'chamber': ('django.db.models.fields.IntegerField', [], {}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idx': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'num_seats': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'openstates_boundary_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'openstates_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'MA'", 'max_length': '2'})
        },
        u'voterguide.election': {
            'Meta': {'ordering': "[u'-is_active', u'election_date']", 'object_name': 'Election'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'election_date': ('django.db.models.fields.DateField', [], {}),
            'election_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'MA'", 'max_length': '2'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': "'2014'"})
        },
        u'voterguide.office': {
            'Meta': {'ordering': "[u'-priority']", 'object_name': 'Office'},
            'chamber': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'voterguide.person': {
            'Meta': {'ordering': "[u'last_name', u'first_name']", 'object_name': 'Person'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'middle': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'openstates_legid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'photo_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'suffixes': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'voterguide.race': {
            'Meta': {'ordering': "[u'state', u'election', u'office', u'district']", 'object_name': 'Race'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voterguide.District']", 'null': 'True', 'blank': 'True'}),
            'election': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voterguide.Election']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'office': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voterguide.Office']"}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'MA'", 'max_length': '2'})
        }
    }

    complete_apps = ['voterguide']