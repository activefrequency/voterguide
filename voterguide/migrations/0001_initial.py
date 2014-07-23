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


    def backwards(self, orm):
        # Deleting model 'Election'
        db.delete_table(u'voterguide_election')

        # Deleting model 'District'
        db.delete_table(u'voterguide_district')

        # Deleting model 'Office'
        db.delete_table(u'voterguide_office')

        # Deleting model 'Race'
        db.delete_table(u'voterguide_race')


    models = {
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
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'voterguide.race': {
            'Meta': {'object_name': 'Race'},
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