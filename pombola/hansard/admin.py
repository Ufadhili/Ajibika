from django.contrib import admin
import models

from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin

import datetime

# from django import forms
from django.conf.urls import patterns
# from django.contrib import admin
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django.shortcuts  import  redirect
from django.template   import RequestContext

import models
from pprint import pprint

# from django.contrib.gis import db
# from django.core.urlresolvers import reverse
# from django.contrib.contenttypes.generic import GenericTabularInline
# from django import forms
# 
# def create_admin_link_for(obj, link_text):
#     return u'<a href="%s">%s</a>' % ( obj.get_admin_url(), link_text )


class SourceAdmin(admin.ModelAdmin):
    list_display  = [ 'name', 'date', 'last_processing_success', 'last_processing_attempt' ]
    list_filter = ('date', 'last_processing_success')
    date_hierarchy = 'date'
    

class VenueAdmin(admin.ModelAdmin):
    list_display  = [ 'slug', 'name' ]


class SittingAdmin(admin.ModelAdmin):
    list_display  = [ 'start_date', 'start_time', 'end_date', 'end_time', 'source' ]
    list_filter = ['start_date']
    date_hierarchy = 'start_date'
    

class EntryAdmin(admin.ModelAdmin):
    list_display  = [ 'sitting', 'type', 'speaker_name', 'speaker',  '__unicode__' ]
    

# # When we have Django 1.4
# from django.contrib.admin import SimpleListFilter
# 
# class AliasStatusListFilter(SimpleListFilter):
#     title = _('alias status')
#     parameter_name = 'status'
# 
#     def lookups(self, request, model_admin):
#         return (
#             ('unassigned', 'unassigned'),
#             # ('90s', _('in the nineties')),
#         )
# 
#     def queryset(self, request, queryset):
#         if self.value() == 'unassigned':
#             return queryset.unassigned()


class AliasAdmin(admin.ModelAdmin):
    search_fields = [ 'alias', 'person__legal_name' ]
    list_filter  = [
        'ignored',
        # AliasStatusListFilter,  # Django 1.4
    ]
    list_display = [ 'alias', 'person', 'ignored', 'created' ]
    form = make_ajax_form(
        models.Alias,
        {
            'person':       'person_name',
        }
    )    

    actions = ["ignore_aliases",]
    
    def ignore_aliases(self, request, queryset):
        for alias in queryset:
            alias.ignored = True
            alias.save()

        self.message_user(request, "Ignored the aliases")
    ignore_aliases.short_description = "Ignore the selected aliases"
    

    def get_urls(self):
        urls = super(AliasAdmin, self).get_urls()
        my_urls = patterns('',
            ( r'^next_unassigned/$', self.next_unassigned ),
        )
        return my_urls + urls
        

    @method_decorator(staff_member_required)
    def next_unassigned(self, request):

        # Select the unassigned, and order so that most recently updated come
        # last. This prevents the same one coming back again and again if it
        # cannot be resolved (eg if it is ambiguous). Partial fix for that
        # problem - better would be a 'cant_be_done' flag or similar, or date
        # ranges so that 'Mr. Foo' from 1999 to 2003 is one person, and 2004
        # onwards another. Not implemented now as it is not certain that this
        # is actually a problem.
        unassigned = models.Alias.objects.all().unassigned().order_by('-created')
        

        try:
            alias = unassigned[0]
            return redirect( '/admin/hansard/alias/' + str(alias.id) + '/' )
        except IndexError:
            return render_to_response(
                'admin/hansard/alias',
                {},
                context_instance=RequestContext(request)
            )

admin.site.register( models.Source,  SourceAdmin )
admin.site.register( models.Venue,   VenueAdmin )
admin.site.register( models.Sitting, SittingAdmin )
admin.site.register( models.Entry,   EntryAdmin )
admin.site.register( models.Alias,   AliasAdmin )
