# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DocumentKind'
        db.create_table(u'ajibika_resources_documentkind', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type_of_document', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('summary', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'ajibika_resources', ['DocumentKind'])

        # Adding model 'Video'
        db.create_table(u'ajibika_resources_video', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('summary', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('youtube_link', self.gf('django.db.models.fields.URLField')(max_length=400)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'ajibika_resources', ['Video'])

        # Adding model 'Image'
        db.create_table(u'ajibika_resources_image', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('file', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('summary', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'ajibika_resources', ['Image'])

        # Adding model 'Partner'
        db.create_table(u'ajibika_resources_partner', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('partner_name', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('summary', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'ajibika_resources', ['Partner'])

        # Adding model 'AboutAjibika'
        db.create_table(u'ajibika_resources_aboutajibika', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('about_us', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('terms_and_condition', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'ajibika_resources', ['AboutAjibika'])

        # Adding model 'Document'
        db.create_table(u'ajibika_resources_document', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('document_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ajibika_resources.DocumentKind'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('summary', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'ajibika_resources', ['Document'])


    def backwards(self, orm):
        # Deleting model 'DocumentKind'
        db.delete_table(u'ajibika_resources_documentkind')

        # Deleting model 'Video'
        db.delete_table(u'ajibika_resources_video')

        # Deleting model 'Image'
        db.delete_table(u'ajibika_resources_image')

        # Deleting model 'Partner'
        db.delete_table(u'ajibika_resources_partner')

        # Deleting model 'AboutAjibika'
        db.delete_table(u'ajibika_resources_aboutajibika')

        # Deleting model 'Document'
        db.delete_table(u'ajibika_resources_document')


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
        u'ajibika_resources.partner': {
            'Meta': {'object_name': 'Partner'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'partner_name': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
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