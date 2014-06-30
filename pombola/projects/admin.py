from django.contrib import admin
import models

class ProjectAdmin(admin.ModelAdmin):
    list_display  = [ 'county', 'project_name' ]
    search_fields = [ 'county__name', 'project_name' ]
    

admin.site.register( models.Project, ProjectAdmin )
