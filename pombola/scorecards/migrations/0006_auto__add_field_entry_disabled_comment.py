# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Entry.disabled_comment'
        db.add_column('scorecards_entry', 'disabled_comment', self.gf('django.db.models.fields.CharField')(default='', max_length=300, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Entry.disabled_comment'
        db.delete_column('scorecards_entry', 'disabled_comment')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'scorecards.category': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Category'},
            '_description_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 2, 8, 13, 41, 48, 147077)', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('markitup.fields.MarkupField', [], {'no_rendered_field': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'synopsis': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 2, 8, 13, 41, 48, 147132)', 'auto_now': 'True', 'blank': 'True'})
        },
        'scorecards.entry': {
            'Meta': {'ordering': "('-date', 'category')", 'unique_together': "(('content_type', 'object_id', 'category', 'date'),)", 'object_name': 'Entry'},
            '_equivalent_remark_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            '_extended_remark_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecards.Category']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 2, 8, 13, 41, 48, 147852)', 'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'disabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'disabled_comment': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300', 'blank': 'True'}),
            'equivalent_remark': ('markitup.fields.MarkupField', [], {'max_length': '400', 'no_rendered_field': 'True', 'blank': 'True'}),
            'extended_remark': ('markitup.fields.MarkupField', [], {'max_length': '1000', 'no_rendered_field': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'remark': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'score': ('django.db.models.fields.IntegerField', [], {}),
            'source_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 2, 8, 13, 41, 48, 147880)', 'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['scorecards']
