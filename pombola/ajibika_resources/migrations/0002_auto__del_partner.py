# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Partner'
        db.delete_table(u'ajibika_resources_partner')


    def backwards(self, orm):
        # Adding model 'Partner'
        db.create_table(u'ajibika_resources_partner', (
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True)),
            ('partner_name', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('summary', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'ajibika_resources', ['Partner'])


    models = {
        u'ajibika_resources.aboutajibika': {
            'Meta': {'object_name': 'AboutAjibika'},
            'about_us': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'terms_and_condition': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'ajibika_resources.document': {
            'Meta': {'object_name': 'Document'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'document_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ajibika_resources.DocumentKind']"}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'ajibika_resources.documentkind': {
            'Meta': {'object_name': 'DocumentKind'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'type_of_document': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'ajibika_resources.image': {
            'Meta': {'object_name': 'Image'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '400'})
        },
        u'ajibika_resources.video': {
            'Meta': {'object_name': 'Video'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'youtube_link': ('django.db.models.fields.URLField', [], {'max_length': '400'})
        }
    }

    complete_apps = ['ajibika_resources']