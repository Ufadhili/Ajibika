from django.contrib import admin
import models

class VideoAdmin(admin.ModelAdmin):
	model = models.Video
	list_display = ['county', 'title', 'video_link']
	prepopulated_fields = {"slug": ["title"]} 

	def video_link(self, obj):
		return '<a href="%s">%s</a>' % (obj.youtube_link, obj.youtube_link)
	video_link.allow_tags = True

admin.site.register( models.Video, VideoAdmin )
