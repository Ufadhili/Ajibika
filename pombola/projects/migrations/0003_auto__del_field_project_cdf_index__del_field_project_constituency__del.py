# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Project.cdf_index'
        db.delete_column(u'projects_project', 'cdf_index')

        # Deleting field 'Project.constituency'
        db.delete_column(u'projects_project', 'constituency_id')

        # Deleting field 'Project.mtfe_sector'
        db.delete_column(u'projects_project', 'mtfe_sector')

        # Adding field 'Project.county'
        db.add_column(u'projects_project', 'county',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['core.Place']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Project.cdf_index'
        db.add_column(u'projects_project', 'cdf_index',
                      self.gf('django.db.models.fields.IntegerField')(default=12345, unique=True),
                      keep_default=False)

        # Adding field 'Project.constituency'
        db.add_column(u'projects_project', 'constituency',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['core.Place']),
                      keep_default=False)

        # Adding field 'Project.mtfe_sector'
        db.add_column(u'projects_project', 'mtfe_sector',
                      self.gf('django.db.models.fields.CharField')(default='no idea', max_length=400),
                      keep_default=False)

        # Deleting field 'Project.county'
        db.delete_column(u'projects_project', 'county_id')


    models = {
        u'core.organisation': {
            'Meta': {'ordering': "['slug']", 'object_name': 'Organisation'},
            '_summary_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ended': ('django_date_extensions.fields.ApproximateDateField', [], {'max_length': '10', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.OrganisationKind']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200'}),
            'started': ('django_date_extensions.fields.ApproximateDateField', [], {'max_length': '10', 'blank': 'True'}),
            'summary': ('markitup.fields.MarkupField', [], {'default': "''", 'no_rendered_field': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'core.organisationkind': {
            'Meta': {'ordering': "['slug']", 'object_name': 'OrganisationKind'},
            '_summary_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200'}),
            'summary': ('markitup.fields.MarkupField', [], {'default': "''", 'no_rendered_field': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'core.parliamentarysession': {
            'Meta': {'ordering': "['start_date']", 'object_name': 'ParliamentarySession'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'house': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Organisation']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapit_generation': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'core.place': {
            'Meta': {'ordering': "['slug']", 'object_name': 'Place'},
            '_summary_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.PlaceKind']"}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'mapit_area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mapit.Area']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'organisation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Organisation']", 'null': 'True', 'blank': 'True'}),
            'parent_place': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child_places'", 'null': 'True', 'to': u"orm['core.Place']"}),
            'parliamentary_session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.ParliamentarySession']", 'null': 'True', 'blank': 'True'}),
            'shape_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200'}),
            'summary': ('markitup.fields.MarkupField', [], {'default': "''", 'no_rendered_field': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'core.placekind': {
            'Meta': {'ordering': "['slug']", 'object_name': 'PlaceKind'},
            '_summary_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'plural_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200'}),
            'summary': ('markitup.fields.MarkupField', [], {'default': "''", 'no_rendered_field': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'mapit.area': {
            'Meta': {'ordering': "('name', 'type')", 'object_name': 'Area'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'areas'", 'null': 'True', 'to': u"orm['mapit.Country']"}),
            'generation_high': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'final_areas'", 'null': 'True', 'to': u"orm['mapit.Generation']"}),
            'generation_low': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'new_areas'", 'null': 'True', 'to': u"orm['mapit.Generation']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'}),
            'parent_area': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['mapit.Area']"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'areas'", 'to': u"orm['mapit.Type']"})
        },
        u'mapit.country': {
            'Meta': {'object_name': 'Country'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'mapit.generation': {
            'Meta': {'object_name': 'Generation'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'mapit.type': {
            'Meta': {'object_name': 'Type'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '500'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'projects.project': {
            'Meta': {'ordering': "['-total_cost']", 'object_name': 'Project'},
            'activity_to_be_done': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'county': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Place']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'econ1': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'econ2': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'estimated_cost': ('django.db.models.fields.FloatField', [], {}),
            'expected_output': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'first_funding_year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'location_name': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'project_name': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'remarks': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'sector': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'total_cost': ('django.db.models.fields.FloatField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['projects']