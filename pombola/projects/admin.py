from django.contrib import admin
import models
from pombola.images.admin import ImageAdminInline
from pombola.documents.admin import DocumentAdminInline


class ProjectDocumentInline(admin.StackedInline):
	model = models.ProjectDocument
	extra = 0

class ProjectVideoInline(admin.StackedInline):
	model = models.ProjectVideo
	extra = 0


class ProjectAdmin(admin.ModelAdmin):
    list_display  = [ 'county', 'project_name', 'status' ]
    search_fields = [ 'county__name', 'project_name' ]
    prepopulated_fields = {"slug": ["project_name"]}
    inlines = [
	    ProjectDocumentInline,
	    ImageAdminInline,	   
	    ProjectVideoInline
    ]
    

admin.site.register( models.Project, ProjectAdmin )
