# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Candidate.party'
        db.alter_column(u'voterguide_candidate', 'party', self.gf('django.db.models.fields.CharField')(max_length=2, null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Candidate.party'
        raise RuntimeError("Cannot reverse this migration. 'Candidate.party' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Candidate.party'
        db.alter_column(u'voterguide_candidate', 'party', self.gf('django.db.models.fields.CharField')(max_length=2))

    models = {
        u'voterguide.candidate': {
            'Meta': {'ordering': "[u'race__state', u'race__election', u'race__office', u'race__district', u'person__last_name', u'person__first_name']", 'object_name': 'Candidate'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_endorsed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_incumbent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_pro': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'party': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voterguide.Person']"}),
            'race': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voterguide.Race']"}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'winner': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'voterguide.district': {
            'Meta': {'ordering': "[u'chamber', u'idx', u'code', u'name']", 'object_name': 'District'},
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
            'blurb': ('django.db.models.fields.TextField', [], {'max_length': '500', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'middle': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'openstates_legid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'photo_url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'suffixes': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'voterguide.race': {
            'Meta': {'ordering': "[u'state', u'election', u'office', u'district']", 'object_name': 'Race'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voterguide.District']", 'null': 'True', 'blank': 'True'}),
            'election': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voterguide.Election']"}),
            'has_endorsement': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'office': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voterguide.Office']"}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'MA'", 'max_length': '2'})
        }
    }

    complete_apps = ['voterguide']