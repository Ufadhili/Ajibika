from django.contrib import admin
import models



class VideoAdmin(admin.ModelAdmin):
	list_display = ['title', 'youtube_link', 'created']
	search_fields = ['title']
	prepopulated_fields = {'slug': ['title']}

admin.site.register(models.Video, VideoAdmin)


class DocumentAdmin(admin.ModelAdmin):
	list_display = ['title', 'document_type', 'created']
	search_fields = ['title']
	prepopulated_fields = {'slug': ['title']}

admin.site.register(models.Document, DocumentAdmin)

class ImageAdmin(admin.ModelAdmin):
	list_display = ['title', 'created']

class DocumentKindAdmin(admin.ModelAdmin):
	list_display = ['type_of_document', 'summary']

admin.site.register(models.DocumentKind, DocumentKindAdmin)