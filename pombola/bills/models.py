from django.db import models
import datetime

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

from pombola.core.models import Place



class Bill(models.Model):	
    created = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now)
    updated = models.DateTimeField(auto_now=True, default=datetime.datetime.now)
    county = models.ForeignKey(Place)
    title = models.CharField(max_length=1000)
    summary = models.TextField(blank=True)
    slug = models.SlugField( unique=True )
    file = models.FileField( upload_to='file_archive' )

    def __unicode__(self):
        return self.slug

    @models.permalink
    def get_absolute_url(self):
        return ( 'file_archive', [ self.slug ] )
    

