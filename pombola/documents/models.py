from django.db import models
import datetime

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

from pombola.core.models import Place


class Document(models.Model):
	BILL = 'CBL'
	BUDGET = 'CBT'
	PLAN = 'CPN'
	TRANSCRIPT = 'CTT'
	PROJECT = 'CPR'
	OTHER = 'COR'
	COUNTY_DOCUMENT_CHOICES = (	
					('CBL', 'Bill'),
					('CBT','Budget'),
					('CPN','Plan'),
					('CTT','Transcript'),
					('CPR', 'Project'),
					('COR','Other'),
			)
	created = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now)
	updated = models.DateTimeField(auto_now=True, default=datetime.datetime.now)
	county = models.ForeignKey(Place)
	document_type = models.CharField(max_length=3, choices=COUNTY_DOCUMENT_CHOICES,default=BILL)
	title = models.CharField(max_length=1000)
	slug = models.SlugField( unique=True )
	summary = models.TextField(blank=True)	
	file = models.FileField( upload_to='file_archive' )

	def __unicode__(self):
		return self.slug

	@models.permalink
	def get_absolute_url(self):
		return ( 'file_archive', [ self.slug ] )
    


