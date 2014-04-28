import re
import sys
import simplejson

from django.http import HttpResponse
from django.shortcuts  import render_to_response, get_object_or_404, redirect
from django.template   import RequestContext
from django.conf import settings

from django.views.generic import TemplateView

from pombola.core import models

from haystack.query import SearchQuerySet

from sorl.thumbnail import get_thumbnail
from .geocoder import geocoder


class GeocoderView(TemplateView):
    template_name = "search/location.html"

    # This should really be set somewhere is the app's config.
    # See https://github.com/mysociety/pombola/issues/829
    country_app_to_alpha2_mapping = {
        # http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
        "south_africa": "za",
        "kenya":        "ke",
        "zimbabwe":     "zw",
        "nigeria":      "ng",
        "libya":        "ly",
    }

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(GeocoderView, self).get_context_data()

        country_alpha2 = self.country_app_to_alpha2_mapping.get(settings.COUNTRY_APP)

        if not country_alpha2:
            # search can still go ahead, but it will not be restricted to the country expected
            sys.stderr.write("Need to add country code for {0} to 'search.views.GeocoderView'".format(settings.COUNTRY_APP))

        query = self.request.GET.get('q')
        if query:
            context['query'] = query
            context['geocoder_results'] = geocoder(country=country_alpha2, q=query)

        return context


known_kinds = {
    'person': models.Person,
    'place':  models.Place,
}

def places_ordered_by_session(place_a, place_b):
    """Return True if both places have sessions and place_b's is later"""
    a_session = place_a.parliamentary_session
    b_session = place_b.parliamentary_session
    if not (a_session and b_session):
        return False
    return a_session.end_date < b_session.end_date

def remove_duplicate_places(response_data):
    """Remove all but the newest of places with indistinguishable labels

    We have a slightly unpleasant problem where consituencies that
    have the same name from one parliament to the next appear twice
    with exactly the same label - people get confused if they pick the
    old one and don't find their aspirants.  We could exclude all
    older constituencies, but for people who don't know that their
    constituency name has changed, it's potentially useful to still
    have the old name returned in results.  So, look for duplicate
    labels, and (if they're places) delete the one from the older
    parliamentary session."""

    indices_to_remove = []
    previous_label_index = {}

    for i, result in enumerate(response_data):
        this_label = result['label']
        this_object = result['object']
        if (this_label in previous_label_index) and type(this_object) == models.Place:
            previous_i = previous_label_index[this_label]
            if places_ordered_by_session(response_data[previous_i]['object'], this_object):
                indices_to_remove.append(previous_i)
                previous_label_index[this_label] = i
            else:
                indices_to_remove.append(i)
        else:
            previous_label_index[this_label] = i

    # Now remove those marked for deletion:
    indices_to_remove.sort(reverse=True)
    for index_to_remove in indices_to_remove:
        del response_data[index_to_remove]

def autocomplete(request):
    """Return autocomplete JSON results"""

    term = request.GET.get('term','').strip()
    response_data = []

    if len(term):

        # Does not work - probably because the FLAG_PARTIAL is not set on Xapian
        # (trying to set it in settings.py as documented appears to have no effect)
        # sqs = SearchQuerySet().autocomplete(name_auto=term)

        # Split the search term up into little bits
        terms = re.split(r'\s+', term)

        # Build up a query based on the bits
        sqs = SearchQuerySet()
        for bit in terms:
            # print "Adding '%s' to the '%s' query" % (bit,term)
            sqs = sqs.filter_and(
                name_auto__startswith = sqs.query.clean( bit )
            )

        # If we have a kind then filter on that too
        model_kind = request.GET.get('model', None)
        if model_kind:
            model = known_kinds.get(model_kind, None)
            if model:
                sqs = sqs.models(model)

        # collate the results into json for the autocomplete js
        for result in sqs.all()[0:10]:

            object = result.object
            css_class = object.css_class()

            # use the specific field if it has one
            if hasattr(object, 'name_autocomplete_html'):
                label = object.name_autocomplete_html
            else:
                label = object.name

            image_url = None
            if hasattr(object, 'primary_image'):
                image = object.primary_image()
                if image:
                    image_url = get_thumbnail(image, '16x16', crop="center").url

            if not image_url:
                image_url = "/static/images/" + css_class + "-16x16.jpg"

            response_data.append({
                'url':   object.get_absolute_url(),
                'label': '<img height="16" width="16" src="%s" /> %s' % (image_url, label),
                'type':  css_class,
                'value': object.name,
                'object': object
            })

    remove_duplicate_places(response_data)

    # Remove the 'object' elements before returning the response:
    for d in response_data:
        del d['object']

    # send back the results as JSON
    return HttpResponse(
        simplejson.dumps(response_data),
        content_type='application/json',
    )

