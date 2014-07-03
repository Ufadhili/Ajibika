import time
import calendar
import datetime
import random

from django.db.models import Count
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts  import render_to_response, get_object_or_404, redirect
from django.template   import RequestContext
from django.views.decorators.cache import cache_control, never_cache
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.core.cache import cache
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from pombola.core import models
from pombola.info.models import InfoPage
from pombola.documents.models import Document


class HomeView(TemplateView):

    template_name = 'ajibika/index.html'

    def get_context_data(self, **kwargs):

        context = super(HomeView, self).get_context_data(**kwargs)

        # before, after = (self.request.GET.get(k) for k in ('before', 'after'))
        # current_slug = before or after

        # context['featured_person'] = \
        #     models.Person.objects.get_next_featured(current_slug,
        #                                             want_previous=before)

        # For the election homepage produce a list of all the featured people.
        # Shuffle it each time to avoid any bias.
        # context['featured_persons'] = list(models.Person.objects.get_featured())
        context['counties'] = models.Place.objects.filter(kind__slug='county')
        # random.shuffle(context['featured_persons'])

        return context

class AboutAjibikaView(TemplateView):

    template_name = 'ajibika/about_ajibika.html'

    def get_context_data(self, **kwargs):
        context = super(AboutAjibikaView, self).get_context_data(**kwargs)
        context['counties'] = models.Place.objects.filter(kind__slug='county')        
        return context


class OrganisationList(ListView):
    model = models.Organisation

class ProfileDetails(DetailView):
    model = models.Person
    # template_name = 'ajibika/profile2.html'

class CountyExecutive(DetailView):
    model = models.Place
    context_object_name = "county"
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CountyExecutive, self).get_context_data(**kwargs)
        context['persons'] = models.Place.objects.get(slug=self.kwargs['slug']).county_executive()
        context['category'] = 'County Executive'
        context['counties'] = models.Place.objects.filter(kind__slug='county')
        context['governor'] = self.object.current_county_governor()
        context['deputy_governor'] = self.object.current_county_deputy_governor()
        context['senator'] = self.object.current_county_senator()
        context['speaker'] = self.object.current_county_assembly_speaker()
        return context

class CountyAssembly(DetailView):
    model = models.Place
    context_object_name = "county"
    
    def get_context_data(self, **kwargs):
        context = super(CountyAssembly, self).get_context_data(**kwargs)
        context['persons'] = models.Place.objects.get(slug=self.kwargs['slug']).county_assembly()
        context['category'] = 'County Assembly'
        context['counties'] = models.Place.objects.filter(kind__slug='county')
        context['governor'] = self.object.current_county_governor()
        context['deputy_governor'] = self.object.current_county_deputy_governor()
        context['senator'] = self.object.current_county_senator()
        context['speaker'] = self.object.current_county_assembly_speaker()
        return context

class AboutCounty(DetailView):
    model = models.Place
    context_object_name = 'county'

    def get_context_data(self, **kwargs):
        context = super(AboutCounty, self).get_context_data(**kwargs)
        context['about'] = models.Place.objects.get(slug=self.kwargs['slug'])
        context['counties'] = models.Place.objects.filter(kind__slug='county')
        context['governor'] = self.object.current_county_governor()
        context['deputy_governor'] = self.object.current_county_deputy_governor()
        context['senator'] = self.object.current_county_senator()
        context['speaker'] = self.object.current_county_assembly_speaker()
        return context

class CountyBills(DetailView):
    model = models.Place
    context_object_name = 'county'

    def get_context_data(self, **kwargs):
        context = super(CountyBills, self).get_context_data(**kwargs)
        context['about'] = models.Place.objects.get(slug=self.kwargs['slug'])
        context['counties'] = models.Place.objects.filter(kind__slug='county')
        context['governor'] = self.object.current_county_governor()
        context['deputy_governor'] = self.object.current_county_deputy_governor()
        context['senator'] = self.object.current_county_senator()
        context['bills'] = self.object.document_set.filter(document_type='CBL')
        context['speaker'] = self.object.current_county_assembly_speaker()

        return context

class CountyProjects(DetailView):
    model = models.Place
    context_object_name = 'county'

    def get_context_data(self, **kwargs):
        context = super(CountyProjects, self).get_context_data(**kwargs)
        context['about'] = models.Place.objects.get(slug=self.kwargs['slug'])
        context['counties'] = models.Place.objects.filter(kind__slug='county')
        context['governor'] = self.object.current_county_governor()
        context['deputy_governor'] = self.object.current_county_deputy_governor()
        context['senator'] = self.object.current_county_senator()
        context['speaker'] = self.object.current_county_assembly_speaker()
        return context

class CountyPlan(DetailView):
    model = models.Place
    context_object_name = 'county'

    def get_context_data(self, **kwargs):
        context = super(CountyPlan, self).get_context_data(**kwargs)
        context['about'] = models.Place.objects.get(slug=self.kwargs['slug'])
        context['counties'] = models.Place.objects.filter(kind__slug='county')
        context['governor'] = self.object.current_county_governor()
        context['deputy_governor'] = self.object.current_county_deputy_governor()
        context['senator'] = self.object.current_county_senator()
        context['plans'] = self.object.document_set.filter(document_type='CPN')
        context['speaker'] = self.object.current_county_assembly_speaker()

        return context

class CountyBudget(DetailView):
    model = models.Place
    context_object_name = 'county'

    def get_context_data(self, **kwargs):
        context = super(CountyBudget, self).get_context_data(**kwargs)
        context['about'] = models.Place.objects.get(slug=self.kwargs['slug'])
        context['counties'] = models.Place.objects.filter(kind__slug='county')
        context['governor'] = self.object.current_county_governor()
        context['deputy_governor'] = self.object.current_county_deputy_governor()
        context['senator'] = self.object.current_county_senator()
        context['budgets'] = self.object.document_set.filter(document_type='CBT')
        context['speaker'] = self.object.current_county_assembly_speaker()

        return context

class CountyTranscripts(DetailView):
    model = models.Place
    context_object_name = 'county'

    def get_context_data(self, **kwargs):
        context = super(CountyTranscripts, self).get_context_data(**kwargs)
        context['about'] = models.Place.objects.get(slug=self.kwargs['slug'])
        context['counties'] = models.Place.objects.filter(kind__slug='county')
        context['governor'] = self.object.current_county_governor()
        context['deputy_governor'] = self.object.current_county_deputy_governor()
        context['senator'] = self.object.current_county_senator()
        context['speaker'] = self.object.current_county_assembly_speaker()
        return context
        
class CountyOtherDocs(DetailView):
    model = models.Place
    context_object_name = 'county'

    def get_context_data(self, **kwargs):
        context = super(CountyOtherDocs, self).get_context_data(**kwargs)
        context['about'] = models.Place.objects.get(slug=self.kwargs['slug'])
        context['counties'] = models.Place.objects.filter(kind__slug='county')
        context['governor'] = self.object.current_county_governor()
        context['deputy_governor'] = self.object.current_county_deputy_governor()
        context['senator'] = self.object.current_county_senator()

        context['other_docs'] = self.object.document_set.filter(document_type='COR')

        context['speaker'] = self.object.current_county_assembly_speaker()

        return context

class PersonDetail(DetailView):
    model = models.Person
    template_name = 'ajibika/profile2.html'



    def get(self, request, *args, **kwargs):
        # Check if this is old slug for redirection:
        slug = kwargs['slug']
        try:
            sr = models.SlugRedirect.objects.get(content_type=ContentType.objects.get_for_model(models.Person),
                                                 old_object_slug=slug)
            return redirect(sr.new_object)
        # Otherwise look up the slug as normal:
        except models.SlugRedirect.DoesNotExist:
            return super(PersonDetail, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context  = super(PersonDetail, self).get_context_data(**kwargs)
        context['county'] = self.object.constituencies()[0]
        county = self.object.constituencies()[0]
        context['counties'] = models.Place.objects.filter(kind__slug='county')
        context['coalitions'] = self.object.coalitions()
        context['position'] = self.object.politician_positions()[0]
        context['about'] = models.Place.objects.get(slug=county.slug)
        context['counties'] = models.Place.objects.filter(kind__slug='county')
        context['governor'] = county.current_county_governor()
        context['deputy_governor'] = county.current_county_deputy_governor()
        context['senator'] = county.current_county_senator()
        context['bills'] = county.document_set.filter(document_type='CBT')
        context['speaker'] = county.current_county_assembly_speaker()
        return context

class PersonDetailSub(DetailView):
    model = models.Person


    def get_template_names(self):
        return [ "core/person_%s.html" % self.kwargs['sub_page'] ]

class PlaceDetailView(DetailView):
    model = models.Place
    context_object_name = "county"
    template_name = 'ajibika/index2.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PlaceDetailView, self).get_context_data(**kwargs)
        # context['place_type_count'] = models.Place.objects.filter(kind=self.object.kind).count()
        context['related_people'] = self.object.related_people()
        context['governor'] = self.object.current_county_governor()
        context['deputy_governor'] = self.object.current_county_deputy_governor()
        context['senator'] = self.object.current_county_senator()
        context['bills'] = self.object.document_set.filter(document_type='CBL')
        context['counties'] = models.Place.objects.filter(kind__slug='county')
        context['featured'] = self.object.featured_in_the_county()
        context['images'] = self.object.images.all()[1:]
        context['active_image'] = self.object.images.all()[0]
        return context

class PlaceDetailSub(DetailView):
    model = models.Place
    child_place_grouper = 'parliamentary_session'

    def get_context_data(self, **kwargs):
        context = super(PlaceDetailSub, self).get_context_data(**kwargs)
        context['child_place_grouper'] = self.child_place_grouper
        return context

    def get_template_names(self):
        return [ "core/place_%s.html" % self.kwargs['sub_page'] ]

class PlaceKindList(ListView):
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        session_slug = self.kwargs.get('session_slug')

        if slug and slug != 'all':
            self.kind = get_object_or_404(
                models.PlaceKind,
                slug=slug
            )
            queryset = self.kind.place_set.all()
        else:
            self.kind = None
            queryset = models.Place.objects.all()

        if session_slug:
            self.session = get_object_or_404(
                models.ParliamentarySession,
                slug=session_slug
            )
        else:
            self.session = None

        # If this is a PlaceKind with parliamentary sessions, but a
        # particular one hasn't been specified, make the default either
        # the current session, or the most recent one if there is no
        # current session.  (This is largely to make any old bookmarked
        # links to (e.g.) /place/is/constituency/ still work.)

        if self.kind and not self.session:
            sessions = list(self.kind.parliamentary_sessions())
            if sessions:
                today = datetime.date.today()
                current_sessions = [s for s in sessions if s.covers_date(today)]
                if current_sessions:
                    self.session = current_sessions[0]
                else:
                    self.session = sessions[-1]

        if queryset and self.session:
            queryset = queryset.filter(parliamentary_session=self.session)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(PlaceKindList, self).get_context_data(**kwargs)
        context.update(
            kind = self.kind,
            selected_session = self.session,
            all_kinds = models.PlaceKind.objects.all(),
        )
        return context

def position_pt(request, pt_slug):
    """Show current positions with a given PositionTitle"""
    return position(request, pt_slug)

def position_pt_ok(request, pt_slug, ok_slug):
    """Show current positions with a given PositionTitle and OrganisationKind"""
    return position(request, pt_slug, ok_slug=ok_slug)

def position_pt_ok_o(request, pt_slug, ok_slug, o_slug):
    """Show current positions with a given PositionTitle, OrganisationKind and Organisation"""
    return position(request, pt_slug, ok_slug=ok_slug, o_slug=o_slug)

def position(request, pt_slug, ok_slug=None, o_slug=None):
    title = get_object_or_404(
        models.PositionTitle,
        slug=pt_slug
    )

    page_title = title.name
    if o_slug:
        organisation = get_object_or_404(models.Organisation,
                                         slug=o_slug)
        page_title += " of " + organisation.name
    elif ok_slug:
        organisation_kind = get_object_or_404(models.OrganisationKind,
                                              slug=ok_slug)
        page_title += " of any " + organisation_kind.name

    positions = title.position_set.all().currently_active()
    if ok_slug is not None:
        positions = positions.filter(organisation__kind__slug=ok_slug)
    if o_slug is not None:
        positions = positions.filter(organisation__slug=o_slug)

    # Order by place name unless ordering by person name is requested:
    order = 'place'
    if request.GET.get('order') == 'name':
        order = 'person__legal_name'
    positions = positions.order_by(order)

    positions = positions.select_related('person',
                                         'organisation',
                                         'title',
                                         'place',
                                         'place__kind',
                                         'place__parent_place')

    place_slug = request.GET.get('place_slug')
    if place_slug:
        positions = positions.filter(
            Q(place__slug=place_slug) | Q(place__parent_place__slug=place_slug)
        )

    # see if we should show the grid
    view = request.GET.get('view', 'list')

    if view == 'grid':
        template = 'core/position_detail_grid.html'
        places   = [] # not relevant to this view
    else:
        template = 'core/position_detail.html'

        # Collect all the places those positions refer to:
        child_places = sorted(set(x.place for x in positions if x.place),
                              key=lambda p: p.name)

        # Extract the parents of those places as well:
        parent_place_ids = [x.parent_place.id for x in child_places if (x and x.parent_place)]
        parent_places = models.Place.objects.filter(id__in=parent_place_ids).select_related('kind')

        # combine the places into a single list for the search drop down
        places = []
        places.extend(parent_places)
        places.extend(child_places)

    return render_to_response(
        template,
        {
            'object':     title,
            'page_title': page_title,
            'positions':  positions,
            'order':      request.GET.get('order'),
            'places':     places,
            'place_slug': place_slug,
        },
        context_instance=RequestContext(request)
    )


class OrganisationDetailView(DetailView):
    model = models.Organisation

    def get_context_data(self, **kwargs):
        context = super(OrganisationDetailView, self).get_context_data(**kwargs)
        context['positions'] = self.object.position_set.all().order_by('person__legal_name')
        return context


class OrganisationDetailSub(DetailView):
    model = models.Organisation

    def get_template_names(self):
        return [ "core/organisation_%s.html" % self.kwargs['sub_page'] ]

    def get_context_data(self, **kwargs):
        context = super(OrganisationDetailSub, self).get_context_data(**kwargs)
        # Allow the order that people are listed on the 'people' sub-page
        # of an organisation to be controlled with the 'order' query
        # parameter:
        if self.kwargs['sub_page'] == 'people':
            all_positions = context['all_positions'] = self.object.position_set.all()

            if self.request.GET.get('all'):
                positions = all_positions
            # Limit to those currently active, or inactive
            elif self.request.GET.get('historic'):
                context['historic'] = True
                positions = all_positions.currently_inactive()
            else:
                context['historic'] = False
                positions = all_positions.currently_active()

            if self.request.GET.get('order') == 'place':
                context['sorted_positions'] = positions.order_by_place()
            else:
                context['sorted_positions'] = positions.order_by_person_name()
        return context

class OrganisationKindList(SingleObjectMixin, ListView):
    model = models.OrganisationKind

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=self.model.objects.all())
        return super(OrganisationKindList, self).get(request, *args, **kwargs)

    def get_queryset(self):
        orgs = (
            self.object
                .organisation_set
                .all()
                .annotate(num_positions = Count('position'))
                .order_by('-num_positions', 'name')
        )
        return orgs

    def get_context_data(self, **kwargs):
        context = super(OrganisationKindList, self).get_context_data(**kwargs)
        context['kind'] = self.object
        return context

def parties(request):
    """Show all parties that currently have MPs sitting in parliament"""

    parties = models.Organisation.objects.all().active_parties()

    return render_to_response(
        'core/parties.html',
        {
            'parties': parties,
        },
        context_instance = RequestContext( request ),
    )

def featured_person(request, current_slug, direction):
    """Show featured mp either before or after the current one.
       Returns a random person if current slug doesn't match, although numeric
       slugs are consistent to ease the caching a little (so javascript can make
       random requests that can be cached)."""
    want_previous = direction == 'before'
    featured_person = models.Person.objects.get_next_featured(current_slug, want_previous)
    return render_to_response(
        'core/person_feature.html',
        {
            'featured_person': featured_person,
        },
        context_instance = RequestContext( request ),
    )

# We never want this to be cached
@never_cache
def memcached_status(request):
    """Helper view that let's us check that the values are being stored in the cache, and subsequently purged"""

    cache_key = 'memcached_status'
    now = calendar.timegm( time.gmtime() )
    ttl = 10

    cached = cache.get(cache_key)

    if cached:
        response = "Found %u in cache with key %s, which was %u seconds ago (ttl is %u seconds)" % (cached, cache_key, now - cached, ttl )
    else:
        cache.set( cache_key, now, ttl )
        response = "Value not found in cache with key %s - added %u for %u seconds" % ( cache_key, now, ttl )

    return HttpResponse(
        response,
        content_type='text/plain',
    )


# Template the robots.txt so we can block robots on staging.
@cache_control(max_age=86400, s_maxage=86400, public=True)
def robots(request):
    return render_to_response(
        'robots.txt',
        {
            'staging': settings.STAGING,
        },
        context_instance=RequestContext(request),
        content_type='text/plain',
    )
