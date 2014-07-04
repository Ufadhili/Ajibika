from django.db import models
import datetime

from pombola.core.models import Place

# Create your models here.


class Video(models.Model):
	county = models.ForeignKey(Place)
	title = models.CharField(max_length=400)
	slug = models.SlugField( unique=True )
	summary = models.TextField(blank=True)	
	youtube_link = models.URLField(max_length=400)
	created = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now)
	updated = models.DateTimeField(auto_now=True, default=datetime.datetime.now)

	def __unicode__(self):
		return self.title

