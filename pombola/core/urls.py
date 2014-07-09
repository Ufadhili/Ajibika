from django.conf.urls import patterns, include, url

from django.views.generic import TemplateView, ListView, RedirectView

from pombola.core import models
from pombola.core.views import (HomeView, PlaceDetailView,
    OrganisationList, OrganisationKindList, PlaceKindList, PersonDetail,
    PersonDetailSub, PlaceDetailSub, OrganisationDetailSub, ProfileDetails,
    OrganisationDetailView, CountyExecutive, CountyAssembly, AboutCounty, 
    CountyBills, CountyProjects, CountyPlan, CountyBudget, CountyTranscripts, 
    CountyOtherDocs, CountyGallery)

person_patterns = patterns('pombola.core.views',
    url(r'^$', ProfileDetails.as_view(template_name = 'ajibika/profile2.html'),
        name='profile'), 
    url(r'^all/',
        ListView.as_view(model=models.Person),
        name='person_list'),

    url(
        r'^politicians/',
        # This is what I'd like to have - but as the 'position' path does
        # not exist yet it gets confused. Hardcode instead - this end point
        # should be removed at some point - legacy from the MzKe site.
        # 'url': reverse('position', kwargs={'slug':'mp'}),
        RedirectView.as_view(url='/position/mp', permanent=True),
    ),

    # featured person ajax load
    url(r'^featured/((?P<direction>(before|after))/)?(?P<current_slug>[-\w]+)',
        'featured_person',
        name='featured_person'),

    url(r'^(?P<slug>[-\w]+)/$', PersonDetail.as_view(), name='person'),


  )

# ugly, must be a better way
for sub_page in ['scorecard', 'comments', 'experience', 'appearances', 'contact_details']:
    person_patterns += patterns(
        'pombola.core.views',
        url(
            '^(?P<slug>[-\w]+)/%s/' % sub_page,  # url regex
            PersonDetailSub.as_view(),           # view function
            { 'sub_page': sub_page },            # pass in the 'sub_page' arg
            'person_%s' % sub_page               # url name for {% url ... %} tags
        )
    )



place_patterns = patterns('pombola.core.views',

    url( r'^all/', PlaceKindList.as_view(), name='place_kind_all' ),
    url( r'^is/(?P<slug>[-\w]+)/$', PlaceKindList.as_view(), name='place_kind'     ),
    url( r'^is/(?P<slug>[-\w]+)/(?P<session_slug>[-\w]+)/?', PlaceKindList.as_view(), name='place_kind'     ),
    url(  r'^(?P<slug>[-\w]+)/about/$', 
        AboutCounty.as_view(template_name='ajibika/about.html'), 
        name='about_county', 
        ),
     url(  r'^(?P<slug>[-\w]+)/bills/$', 
        CountyBills.as_view(template_name='ajibika/bills.html'), 
        name='county_bilss', 
        ),
     url(  r'^(?P<slug>[-\w]+)/projects/$', 
        CountyProjects.as_view(template_name='ajibika/projects.html'), 
        name='county_projects', 
        ),
     url(  r'^(?P<slug>[-\w]+)/plan/$', 
        CountyPlan.as_view(template_name='ajibika/plan.html'), 
        name='county_plan', 
        ),
      url(  r'^(?P<slug>[-\w]+)/budget/$', 
        CountyBudget.as_view(template_name='ajibika/budget.html'), 
        name='county_budget', 
        ),
       url(  r'^(?P<slug>[-\w]+)/transcripts/$', 
        CountyTranscripts.as_view(template_name='ajibika/transcripts.html'), 
        name='county_transcripts', 
        ),
       url(  r'^(?P<slug>[-\w]+)/otherdocs/$', 
        CountyOtherDocs.as_view(template_name='ajibika/otherdocs.html'), 
        name='county_otherdocs', 
        ),
       url(  r'^(?P<slug>[-\w]+)/gallery/$', 
        CountyGallery.as_view(template_name='ajibika/county_gallery.html'), 
        name='county_gallery', 
        ),
       url(  r'^(?P<slug>[-\w]+)/news/$', 
        CountyGallery.as_view(template_name='ajibika/county_news.html'), 
        name='county_news', 
        ),

    url(r'^(?P<slug>[-\w]+)/$',
        PlaceDetailView.as_view(),
        name='place'),

    # redirect .../candidates to .../aspirants so that the URL wording matches
    # that on the site. This is to fix originally using the word 'candidates'
    # and can probably be removed at some point when there are no more hits on
    # this path - after July 2013 feels about right.
    url(
        r'^(?P<slug>[-\w]+)/candidates/$',
        RedirectView.as_view(url='/place/%(slug)s/aspirants', permanent=True),
    ),
    url(
        r'^(?P<slug>[-\w]+)/(?P<category>county-executive)/$', 
        CountyExecutive.as_view(template_name='ajibika/profiles.html'), 
        name='county_executive'),
      url(
        r'^(?P<slug>[-\w]+)/(?P<category>county-assembly)/$', 
        CountyAssembly.as_view(template_name='ajibika/profiles.html'), 
        name='county_assembly'),
    )

# ugly, must be a better way
for sub_page in ['aspirants', 'election', 'scorecard', 'comments', 'people', 'places', 'organisations', 'data', 'projects']:
    place_patterns += patterns(
        'pombola.core.views',
        url(
            '^(?P<slug>[-\w]+)/%s/' % sub_page,  # url regex
            PlaceDetailSub.as_view(),            # view function
            { 'sub_page': sub_page },            # pass in the 'sub_page' arg
            'place_%s' % sub_page                # url name for {% url ... %} tags
        )
    )


organisation_patterns = patterns('pombola.core.views',
    url(r'^all/', OrganisationList.as_view(), name='organisation_list'),
    url(r'^is/(?P<slug>[-\w]+)/', OrganisationKindList.as_view(), name='organisation_kind'),
    url(r'^(?P<slug>[-\w]+)/$', OrganisationDetailView.as_view(), name='organisation'),
)

# ugly, must be a better way
for sub_page in ['comments', 'contact_details', 'people']:
    organisation_patterns += patterns(
        'pombola.core.views',
        url(
            '^(?P<slug>[-\w]+)/%s/' % sub_page,  # url regex
            OrganisationDetailSub.as_view(),     # view function
            { 'sub_page': sub_page },            # pass in the 'sub_page' arg
            'organisation_%s' % sub_page         # url name for {% url ... %} tags
        )
    )

urlpatterns = patterns('pombola.core.views',
    # Homepage
    url(r'^$', HomeView.as_view(), name='home'),

    (r'^person/', include(person_patterns)),
    (r'^place/', include(place_patterns)),
    (r'^organisation/', include(organisation_patterns)),
    # (r'^ufadhili/', include(ufadhili.urls)),

    url(r'^position/(?P<pt_slug>[-\w]+)/$', 'position_pt', name='position_pt'),
    url(r'^position/(?P<pt_slug>[-\w]+)/(?P<ok_slug>[-\w]+)/$', 'position_pt_ok', name='position_pt_ok'),
    url(r'^position/(?P<pt_slug>[-\w]+)/(?P<ok_slug>[-\w]+)/(?P<o_slug>[-\w]+)/$', 'position_pt_ok_o', name='position_pt_ok_o'),

    # specials
    url(r'^parties', 'parties', name='parties'),

    # Ajax select
    url(r'^ajax_select/', include('ajax_select.urls')),
)

urlpatterns += patterns('pombola.core.views',
    url(r'^status/memcached/',       'memcached_status', name='memcached_status'),
)

# Make it easy to see the various error pages without having to fiddle with the
# STAGING settings.
urlpatterns += patterns('',
    url(r'^status/down/', TemplateView.as_view(template_name='down.html') ),
    url(r'^status/404/',  TemplateView.as_view(template_name='404.html') ),
    url(r'^status/500/',  TemplateView.as_view(template_name='500.html') ),
)


# We handle the robots here rather than as a static file so that we can send
# different content on a staging server. We don't use direct_to_template as we
# want to set some caching headers too.
urlpatterns += patterns('pombola.core.views',
    url(r'robots.txt', 'robots' ),
)

