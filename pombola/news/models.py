from django.db import models
import datetime
from pombola.core.models import Place
from pombola.videos.models import Video
from pombola.images.models import Image
from django.contrib.contenttypes import generic



# Create your models here.

class NewsEntry(models.Model):
	county = models.ForeignKey(Place)
	title = models.CharField(max_length=400)
	slug = models.SlugField(unique=True)
	message = models.TextField()
	detail_url = models.URLField(max_length=400, blank=True, null=True)
	publication_date = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now)
	updated = models.DateTimeField(auto_now=True, default=datetime.datetime.now)
	images = generic.GenericRelation(Image)

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return "%snews/%s/" % (self.county.get_absolute_url(), self.slug)

	class Meta:
		verbose_name_plural = "News Entries"


class NewsVideo(models.Model):	
    video = models.ForeignKey(Video)
    news_entry = models.ForeignKey('NewsEntry')
