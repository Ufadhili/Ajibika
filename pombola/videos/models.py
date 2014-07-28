from django.db import models
import datetime
import urlparse

from pombola.core.models import Place

# Create your models here.


class Video(models.Model):
	county = models.ForeignKey(Place)
	title = models.CharField(max_length=400)
	slug = models.SlugField( unique=True )
	summary = models.TextField(blank=True)	
	youtube_link = models.URLField(max_length=400, help_text="Please note the url must be in this format http://youtu.be/nkILmshcIeg. Otherwise it will not display for the users.")
	created = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now)
	updated = models.DateTimeField(auto_now=True, default=datetime.datetime.now)

	def __unicode__(self):
		return self.title

	def youtube_embed_link(self):
		url_data = urlparse.urlparse(self.youtube_link)
		path = url_data.path
		url = "//www.youtube.com/embed%s" % (path)
		return url


