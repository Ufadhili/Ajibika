from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^in/(?P<slug>[-\w]+)/', views.in_place, name='project_in_place'),
)
