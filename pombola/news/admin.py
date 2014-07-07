from django.contrib import admin
from pombola.images.admin import ImageAdminInline

import models


class NewsEntryVideoInline(admin.StackedInline):
	model  = models.NewsVideo
	extra = 0



class NewsEntryAdmin(admin.ModelAdmin):
	list_display = ['county', 'title', 'publication_date', 'detail_url']
	search_fields = ['title']
	prepopulated_fields = {'slug': ['title']}
	inlines = [
		ImageAdminInline,
		NewsEntryVideoInline
	]



admin.site.register(models.NewsEntry, NewsEntryAdmin)