import datetime

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

from pombola.core.models import Place
from pombola.documents.models import Document
from django.contrib.contenttypes import generic
from pombola.images.models import HasImageMixin, Image
from pombola.videos.models import Video



class Project(models.Model):
    ONGOING = 'POG'
    PROPOSED = 'PPD'
    COMPLETED = 'PCD'
    STALLED = 'PSD'
    OTHER = 'POR'
    PROJECT_STATUS_CHOICES = ( 
                    ('POG','Ongoing'),
                    ('PPD','Proposed'),
                    ('PCD','Completed'),
                    ('PSD','Stalled'),                    
            )
    created = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now)
    updated = models.DateTimeField(auto_now=True, default=datetime.datetime.now)
    county = models.ForeignKey(Place)
    project_name = models.CharField(max_length=400)
    slug = models.SlugField(max_length=400, unique=True, help_text="created from project name")
    location_name = models.CharField(max_length=400,blank=True, null=True)
    sector = models.CharField(max_length=400, blank=True, null=True)   
    summary = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=3, choices=PROJECT_STATUS_CHOICES,default=ONGOING)    
    images = generic.GenericRelation(Image)    
    estimated_cost = models.FloatField(blank=True, null=True)
    total_cost = models.FloatField(blank=True, null=True)
    first_funding_year = models.IntegerField(blank=True, null=True)
    contractor = models.CharField(max_length=400, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta():
        # NOTE - the templates rely on this default ordering. Really we should
        # use a custom manager and query_set and 'use_for_related_fields = True'
        # but currently Django is broken:
        # https://code.djangoproject.com/ticket/14891
        # The other work-around of creating a method on the place to access the
        # correct manager for the projects is likely to cause confusion.
        ordering = ['-total_cost'] # <--- DO NOT CHANGE

    def get_absolute_url(self):
        slug = self.slug
        county = self.county.slug
        return "place/%s/projects/%s/" % (county, slug)

    def has_images(self):
        return self.images.all().exists()

    def has_documents(self):
        return self.projectdocument_set.all().exists()

    def has_videos(self):
        return self.projectvideo_set.all().exists()


class ProjectDocument(models.Model):
    title = models.CharField(max_length=400)
    file = models.FileField(upload_to='file_archive')
    project = models.ForeignKey('Project')

class ProjectVideo(models.Model):
    video = models.ForeignKey(Video)
    project = models.ForeignKey('Project')