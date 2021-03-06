# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Changing field 'Submission.expected_result'
        db.alter_column('votematch_submission', 'expected_result_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['votematch.Party'], null=True, blank=True))
    
    
    def backwards(self, orm):
        
        # Changing field 'Submission.expected_result'
        db.alter_column('votematch_submission', 'expected_result_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['votematch.Party']))
    
    
    models = {
        'votematch.answer': {
            'Meta': {'object_name': 'Answer'},
            'agreement': ('django.db.models.fields.IntegerField', [], {}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'statement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['votematch.Statement']"}),
            'submission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['votematch.Submission']"})
        },
        'votematch.party': {
            'Meta': {'object_name': 'Party'},
            '_summary_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'quiz': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['votematch.Quiz']"}),
            'summary': ('markitup.fields.MarkupField', [], {'no_rendered_field': 'True'})
        },
        'votematch.quiz': {
            'Meta': {'object_name': 'Quiz'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'})
        },
        'votematch.stance': {
            'Meta': {'object_name': 'Stance'},
            'agreement': ('django.db.models.fields.IntegerField', [], {}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['votematch.Party']"}),
            'statement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['votematch.Statement']"})
        },
        'votematch.statement': {
            'Meta': {'object_name': 'Statement'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'quiz': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['votematch.Quiz']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'votematch.submission': {
            'Meta': {'object_name': 'Submission'},
            'age': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'expected_result': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['votematch.Party']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'quiz': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['votematch.Quiz']"}),
            'token': ('django.db.models.fields.TextField', [], {'default': "'07999077'", 'unique': 'True'})
        }
    }
    
    complete_apps = ['votematch']
