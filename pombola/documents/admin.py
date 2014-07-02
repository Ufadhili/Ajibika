from django.contrib import admin
from pombola.documents import models

class DocumentAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ["title"]}
	list_display  = [ 'title', 'updated', 'created', 'updated', 'county']
	search_fields = [ 'slug' ]
	# exclude = ['slug']


admin.site.register( models.Document, DocumentAdmin )
