from django.contrib import admin
from pombola.bills import models

class BillAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ["title"]}
	list_display  = [ 'title', 'updated', 'created', 'updated', 'county']
	search_fields = [ 'slug' ]


# admin.site.register( models.Bill, BillAdmin )
