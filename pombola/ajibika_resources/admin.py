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

admin.site.register(models.Image, ImageAdmin)

class DocumentKindAdmin(admin.ModelAdmin):
	list_display = ['type_of_document', 'summary']

admin.site.register(models.DocumentKind, DocumentKindAdmin)

class PartnerAdmin(admin.ModelAdmin):
	list_display = ['partner_name', 'website']

admin.site.register(models.Partner, PartnerAdmin)

class AboutAjibikaAdmin(admin.ModelAdmin):
	list_display = ['about_us']

admin.site.register(models.AboutAjibika, AboutAjibikaAdmin)