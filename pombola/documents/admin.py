from django.contrib import admin
from pombola.documents import models
from django.contrib.contenttypes.generic import GenericTabularInline
from sorl.thumbnail.admin import AdminImageMixin
import models


class DocumentAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ["title"]}
	list_display  = [ 'title', 'updated', 'created', 'updated', 'county']
	search_fields = [ 'slug' ]
	# exclude = ['slug']

class DocumentAdminInline(admin.TabularInline):
    model        = models.Document
    

admin.site.register( models.Document, DocumentAdmin )

