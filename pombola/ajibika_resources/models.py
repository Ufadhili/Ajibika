from django.db import models
import datetime

# Create your models here.

class DocumentKind(models.Model):
	type_of_document = models.CharField(max_length=100)
	summary = models.TextField(blank=True)
	
	def __unicode__(self):
		return self.type_of_document

class Video(models.Model):
	title = models.CharField(max_length=400)
	slug = models.SlugField( unique=True )
	summary = models.TextField(blank=True)	
	youtube_link = models.URLField(max_length=400)
	created = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now)
	updated = models.DateTimeField(auto_now=True, default=datetime.datetime.now)


class Image(models.Model):
	title = models.CharField(max_length=400)
	slug = models.SlugField( unique=True )
	created = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now)
	file = models.ImageField(upload_to='file_archive')
	summary = models.TextField(blank=True)

class Partner(models.Model):
	partner_name = models.CharField(max_length=400)
	slug = models.SlugField(unique=True)
	logo = models.ImageField(upload_to='file_archive')
	summary = models.TextField(blank=True)
	website = models.URLField(blank=True)

class AboutAjibika(models.Model):
	about_us = models.TextField(blank=True, help_text="What is Ajibika Platform")
	terms_and_condition = models.TextField(blank=True, help_text="Website's Terms and Conditions")



class Document(models.Model):
	document_type = models.ForeignKey(DocumentKind)
	title = models.CharField(max_length=200)
	slug = models.SlugField( unique=True )
	summary = models.TextField(blank=True)
	created = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now)
	file = models.FileField(upload_to='file_archive')

	def __unicode__(self):
		return self.title

class Meta:
       app_label = 'Devolution Resources'

