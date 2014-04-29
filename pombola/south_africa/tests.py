import re
import os
from datetime import date, time
from StringIO import StringIO
from urlparse import urlparse

from mock import patch

from django.contrib.gis.geos import Polygon, Point
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.core.management import call_command
from django_webtest import WebTest

from mapit.models import Type, Area, Geometry, Generation

from django.conf import settings
from pombola.core import models
import json

from popit.models import Person as PopitPerson, ApiInstance
from speeches.models import Speaker, Section, Speech
from speeches.tests import create_sections
from pombola import south_africa
from pombola.south_africa.views import PersonSpeakerMappings
from instances.models import Instance
from pombola.interests_register.models import Category, Release, Entry, EntryLineItem
from pombola.search.tests.views import fake_geocoder

from nose.plugins.attrib import attr

@attr(country='south_africa')
class HomeViewTest(TestCase):

    def test_homepage_context(self):
        response = self.client.get('/')
        self.assertIn('featured_person', response.context)
        self.assertIn('featured_persons', response.context)
        self.assertIn('news_categories', response.context)

@attr(country='south_africa')
class ConstituencyOfficesTestCase(WebTest):
    def setUp(self):
        self.old_HAYSTACK_SIGNAL_PROCESSOR = settings.HAYSTACK_SIGNAL_PROCESSOR
        settings.HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

        # Mapit Setup
        self.old_srid = settings.MAPIT_AREA_SRID
        settings.MAPIT_AREA_SRID = 4326

        self.generation = Generation.objects.create(
            active=True,
            description="Test generation",
            )

        self.province_type = Type.objects.create(
            code='PRV',
            description='Province',
            )

        self.mapit_test_province = Area.objects.create(
            name="Test Province",
            type=self.province_type,
            generation_low=self.generation,
            generation_high=self.generation,
            )

        self.mapit_test_province_shape = Geometry.objects.create(
            area=self.mapit_test_province,
            polygon=Polygon(((17, -29), (17, -30), (18, -30), (18, -29), (17, -29))),
            )
        # End of Mapit setup.

        (place_kind_province, _) = models.PlaceKind.objects.get_or_create(
            name='Province',
            slug='province',
            )

        models.Place.objects.create(
            name='Test Province',
            slug='test_province',
            kind=place_kind_province,
            mapit_area=self.mapit_test_province,
            )

        org_kind_party = models.OrganisationKind.objects.create(name='Party', slug='party')
        org_kind_constituency_office = models.OrganisationKind.objects.create(name='Constituency Office', slug='constituency-office')
        models.OrganisationKind.objects.create(name='Constituency Area', slug='constituency-area')

        party1 = models.Organisation.objects.create(name='Party1', slug='party1', kind=org_kind_party)
        party2 = models.Organisation.objects.create(name='Party2', slug='party2', kind=org_kind_party)

        p1_office1 = models.Organisation.objects.create(name='Party1: Office1', slug='party1-office1', kind=org_kind_constituency_office)
        p1_office2 = models.Organisation.objects.create(name='Party1: Office2', slug='party1-office2', kind=org_kind_constituency_office)
        p2_office1 = models.Organisation.objects.create(name='Party2: Office1', slug='party2-office1', kind=org_kind_constituency_office)
        p2_office2 = models.Organisation.objects.create(name='Party2: Office2', slug='party2-office2', kind=org_kind_constituency_office)

        orgrelkind_has_office = models.OrganisationRelationshipKind.objects.create(name='has_office')

        office_relationships = (
            (party1, p1_office1),
            (party1, p1_office2),
            (party2, p2_office1),
            (party2, p2_office2),
            )

        for party, office in office_relationships:
            models.OrganisationRelationship.objects.create(organisation_a=party, organisation_b=office, kind=orgrelkind_has_office)

        place_kind_constituency_office = models.PlaceKind.objects.create(name='Constituency Office', slug='constituency-office')
        models.PlaceKind.objects.create(name='Constituency Area', slug='constituency-area')


        # Offices inside the province
        models.Place.objects.create(
            name='Party1: Office1 Place',
            slug='party1-office1-place',
            kind=place_kind_constituency_office,
            location=Point(17.1, -29.1, srid=settings.MAPIT_AREA_SRID),
            organisation=p1_office1,
            )
        models.Place.objects.create(
            name='Party1: Office2 Place',
            slug='party1-office2-place',
            kind=place_kind_constituency_office,
            location=Point(17.2, -29.2, srid=settings.MAPIT_AREA_SRID),
            organisation=p1_office2,
            )
        models.Place.objects.create(
            name='Party2: Office1 Place',
            slug='party2-office1-place',
            kind=place_kind_constituency_office,
            location=Point(17.3, -29.3, srid=settings.MAPIT_AREA_SRID),
            organisation=p2_office1,
            )

        # This office is outside the province
        models.Place.objects.create(
            name='Party2: Office2 Place',
            slug='party2-office2-place',
            kind=place_kind_constituency_office,
            location=Point(16.9, -29, srid=settings.MAPIT_AREA_SRID),
            organisation=p2_office2,
            )


    def test_subplaces_page(self):
        response = self.app.get('/place/test_province/places/')

        content_boxes = response.html.findAll('div', {'class': 'content_box'})

        assert len(content_boxes) == 2, 'We should be seeing two groups of offices.'
        assert len(content_boxes[0].findAll('li')) == 2, 'Box 0 should contain two sections, each with a party office.'
        assert len(content_boxes[1].findAll('li')) == 1, 'Box 1 should contain one sections, as the other party office is outside the box.'

    def tearDown(self):
        settings.MAPIT_AREA_SRID = self.old_srid
        settings.HAYSTACK_SIGNAL_PROCESSOR = self.old_HAYSTACK_SIGNAL_PROCESSOR


@attr(country='south_africa')
class LatLonDetailViewTest(TestCase):
    def test_404_for_incorrect_province_lat_lon(self):
        res = self.client.get(reverse('latlon', kwargs={'lat': '0', 'lon': '0'}))
        self.assertEquals(404, res.status_code)


@attr(country='south_africa')
class SASearchViewTest(WebTest):

    def setUp(self):
        self.search_location_url = reverse('core_geocoder_search')

    def test_search_page_returns_success(self):
        res = self.app.get(reverse('core_search'))
        self.assertEquals(200, res.status_code)

    def get_search_result_list_items(self, query_string):
        response = self.app.get(
            "{0}?q={1}".format(self.search_location_url, query_string))
        results_div = response.html.find('div', class_='geocoded_results')
        return results_div.find('ul').findAll('li')

    @patch('pombola.search.views.geocoder', side_effect=fake_geocoder)
    def test_unknown_place(self, mocked_geocoder):
        lis = self.get_search_result_list_items('anywhere')
        self.assertEqual(len(lis), 0)
        mocked_geocoder.assert_called_once_with(q='anywhere', country='za')

    @patch('pombola.search.views.geocoder', side_effect=fake_geocoder)
    def test_single_result_place(self, mocked_geocoder):
        response = self.app.get(
            "{0}?q={1}".format(self.search_location_url, 'Cape Town'))
        # If there's only a single result (as with Cape Town) we
        # should redirect straight there:
        self.assertEqual(response.status_code, 302)
        path = urlparse(response.location).path
        self.assertEqual(path, '/place/latlon/-33.925,18.424/')
        mocked_geocoder.assert_called_once_with(q='Cape Town', country='za')

    @patch('pombola.search.views.geocoder', side_effect=fake_geocoder)
    def test_multiple_result_place(self, mocked_geocoder):
        lis = self.get_search_result_list_items('Trafford Road')
        self.assertEqual(len(lis), 3)
        self.assertEqual(lis[0].a['href'], '/place/latlon/-29.814,30.839/')
        self.assertEqual(lis[1].a['href'], '/place/latlon/-33.969,18.703/')
        self.assertEqual(lis[2].a['href'], '/place/latlon/-32.982,27.868/')
        mocked_geocoder.assert_called_once_with(q='Trafford Road', country='za')


@attr(country='south_africa')
class SAPersonDetailViewTest(TestCase):
    def setUp(self):
        fixtures = os.path.join(os.path.abspath(south_africa.__path__[0]), 'fixtures')
        popolo_path = os.path.join(fixtures, 'test-popolo.json')
        call_command('core_import_popolo',
            popolo_path,
            commit=True)

        # TODO rewrite this kludge, pending https://github.com/mysociety/popit-django/issues/19
        popolo_io = open(popolo_path, 'r')
        popolo_json = json.load(popolo_io)
        collection_url = 'http://popit.example.com/api/v0.1/'

        api_instance = ApiInstance(url = collection_url)
        api_instance.save()

        for doc in popolo_json['persons']:
            # Add id and url to the doc
            doc['popit_id']  = doc['id']
            url = collection_url + doc['id']
            doc['popit_url'] = url

            person = PopitPerson.update_from_api_results(instance=api_instance, doc=doc)

            instance, _ = Instance.objects.get_or_create(
                label='default',
                defaults = {
                    'title': 'An instance'
                })

            Speaker.objects.create(
                instance = instance,
                name = doc['name'],
                person = person)

        # Create the top level SayIt sections, so that there's no
        # warning when getting the person page:
        create_sections([{'title': u"Hansard"},
                         {'title': u"Committee Minutes"},
                         {'title': u"Questions"}])

    def test_person_to_speaker_resolution(self):
        person = models.Person.objects.get(slug='moomin-finn')
        speaker = PersonSpeakerMappings().pombola_person_to_sayit_speaker(person)
        self.assertEqual( speaker.name, 'Moomin Finn' )

    def test_generation_of_interests_table(self):
        #create data for the test
        person = models.Person.objects.get(slug=u'moomin-finn')

        category1 = Category.objects.create(name=u"Test Category", sort_order=1)
        category2 = Category.objects.create(name=u"Test Category 2", sort_order=2)

        release1 = Release.objects.create(name=u'2013', date=date(2013, 2, 16))
        Release.objects.create(name=u'2012', date=date(2012, 2, 24))

        entry1 = Entry.objects.create(person=person,release=release1,category=category1, sort_order=1)
        entry2 = Entry.objects.create(person=person,release=release1,category=category1, sort_order=2)
        entry3 = Entry.objects.create(person=person,release=release1,category=category2, sort_order=3)

        EntryLineItem.objects.create(entry=entry1,key=u'Field1',value=u'Value1')
        EntryLineItem.objects.create(entry=entry1,key=u'Field2',value=u'Value2')
        EntryLineItem.objects.create(entry=entry2,key=u'Field1',value=u'Value3')
        EntryLineItem.objects.create(entry=entry2,key=u'Field3',value=u'Value4')
        EntryLineItem.objects.create(entry=entry3,key=u'Field4',value=u'Value5')

        #actual output
        context = self.client.get(reverse('person', args=('moomin-finn',))).context

        #expected output
        expected = {
            1: {
                'name': u'2013',
                'categories': {
                    1: {
                        'name': u'Test Category',
                        'headings': [
                            u'Field1',
                            u'Field2',
                            u'Field3'
                        ],
                        'headingindex': {
                            u'Field1': 0,
                            u'Field2': 1,
                            u'Field3': 2
                        },
                        'headingcount': 4,
                        'entries': [
                            [
                                u'Value1',
                                u'Value2',
                                ''
                            ],
                            [
                                u'Value3',
                                '',
                                u'Value4'
                            ]
                        ]
                    },
                    2: {
                        'name': u'Test Category 2',
                        'headings': [
                            u'Field4'
                        ],
                        'headingindex': {
                            u'Field4': 0
                        },
                        'headingcount': 2,
                        'entries': [
                            [
                                u'Value5'
                            ]
                        ]
                    }
                }
            }
        }

        #ideally the following test would be run - however the ordering of entrylineitems appears to be somewhat unpredictable
        #self.assertEqual(context['interests'],expected)

        self.assertEqual(len(context['interests'][1]['categories'][1]['headings']), len(expected[1]['categories'][1]['headings']))
        self.assertEqual(len(context['interests'][1]['categories'][1]['entries']), len(expected[1]['categories'][1]['entries']))
        self.assertEqual(len(context['interests'][1]['categories'][1]['entries'][0]), len(expected[1]['categories'][1]['entries'][0]))
        self.assertEqual(len(context['interests'][1]['categories'][2]['headings']), len(expected[1]['categories'][2]['headings']))
        self.assertEqual(len(context['interests'][1]['categories'][2]['entries']), len(expected[1]['categories'][2]['entries']))
        self.assertEqual(len(context['interests'][1]['categories'][2]['entries'][0]), len(expected[1]['categories'][2]['entries'][0]))


@attr(country='south_africa')
class SAOrganisationPartySubPageTest(TestCase):

    def setUp(self):
        org_kind_party = models.OrganisationKind.objects.create(name='Party', slug='party')
        org_kind_parliament = models.OrganisationKind.objects.create(name='Parliament', slug='parliament')

        party1 = models.Organisation.objects.create(name='Party1', slug='party1', kind=org_kind_party)
        party2 = models.Organisation.objects.create(name='Party2', slug='party2', kind=org_kind_party)
        house1 = models.Organisation.objects.create(name='House1', slug='house1', kind=org_kind_parliament)

        positiontitle1 = models.PositionTitle.objects.create(name='Member', slug='member')
        positiontitle2 = models.PositionTitle.objects.create(name='Delegate', slug='delegate')
        positiontitle3 = models.PositionTitle.objects.create(name='Whip', slug='whip')

        person1 = models.Person.objects.create(legal_name='Person1', slug='person1')
        person2 = models.Person.objects.create(legal_name='Person2', slug='person2')
        person3 = models.Person.objects.create(legal_name='Person3', slug='person3')
        person4 = models.Person.objects.create(legal_name='Person4', slug='person4')
        person5 = models.Person.objects.create(legal_name='Person5', slug='person5')
        person6 = models.Person.objects.create(legal_name='', slug='empty-legal-name')

        models.Position.objects.create(person=person1, organisation=party1, title=positiontitle1)
        models.Position.objects.create(person=person2, organisation=party1, title=positiontitle1)
        models.Position.objects.create(person=person3, organisation=party1, title=positiontitle1)
        models.Position.objects.create(person=person4, organisation=party2, title=positiontitle1)
        models.Position.objects.create(person=person5, organisation=party2, title=positiontitle2)

        models.Position.objects.create(person=person1, organisation=house1, title=positiontitle1)
        models.Position.objects.create(person=person2, organisation=house1, title=positiontitle1)
        models.Position.objects.create(person=person3, organisation=house1, title=positiontitle1, end_date='2013-02-16')
        models.Position.objects.create(person=person4, organisation=house1, title=positiontitle1)
        models.Position.objects.create(person=person5, organisation=house1, title=positiontitle1, end_date='2013-02-16')

        # Add a position for the person with an empty legal name,
        # since this isn't prevented by any validation:
        models.Position.objects.create(person=person6, organisation=party1, title=positiontitle1)
        models.Position.objects.create(person=person6, organisation=house1, title=positiontitle1)

        #check for person who is no longer an official, but still a member
        models.Position.objects.create(person=person1, organisation=house1, title=positiontitle3, end_date='2013-02-16')

    def test_display_current_members(self):
        context1 = self.client.get(reverse('organisation_party', args=('house1', 'party1'))).context
        context2 = self.client.get(reverse('organisation_party', args=('house1', 'party2'))).context

        expected1 = ['<Position:  (Member at House1)>', '<Position: Person1 (Member at House1)>', '<Position: Person2 (Member at House1)>']
        expected2 = ['<Position: Person4 (Member at House1)>']

        self.assertQuerysetEqual(context1['sorted_positions'], expected1)
        self.assertQuerysetEqual(context2['sorted_positions'], expected2)
        self.assertEqual(context1['sorted_positions'][0].person.slug, 'empty-legal-name')
        self.assertEqual(context1['sorted_positions'][1].person.slug, 'person1')
        self.assertEqual(context1['sorted_positions'][2].person.slug, 'person2')
        self.assertEqual(context2['sorted_positions'][0].person.slug, 'person4')

    def test_display_past_members(self):
        context1 = self.client.get(reverse('organisation_party', args=('house1', 'party1')), {'historic': '1'}).context
        context2 = self.client.get(reverse('organisation_party', args=('house1', 'party2')), {'historic': '1'}).context

        expected1 = ['<Position: Person3 (Member at House1)>']
        expected2 = ['<Position: Person5 (Member at House1)>']

        self.assertQuerysetEqual(context1['sorted_positions'], expected1)
        self.assertQuerysetEqual(context2['sorted_positions'], expected2)
        self.assertEqual(context1['sorted_positions'][0].person.slug, 'person3')
        self.assertEqual(context2['sorted_positions'][0].person.slug, 'person5')

    def test_display_all_members(self):
        context1 = self.client.get(reverse('organisation_party', args=('house1', 'party1')), {'all': '1'}).context
        context2 = self.client.get(reverse('organisation_party', args=('house1', 'party2')), {'all': '1'}).context

        expected1 = ['<Position:  (Member at House1)>','<Position: Person1 (Member at House1)>','<Position: Person1 (Whip at House1)>','<Position: Person2 (Member at House1)>','<Position: Person3 (Member at House1)>']
        expected2 = ['<Position: Person4 (Member at House1)>','<Position: Person5 (Member at House1)>']

        self.assertQuerysetEqual(context1['sorted_positions'], expected1)
        self.assertQuerysetEqual(context2['sorted_positions'], expected2)
        self.assertEqual(context1['sorted_positions'][0].person.slug, 'empty-legal-name')
        self.assertEqual(context1['sorted_positions'][1].person.slug, 'person1')
        self.assertEqual(context1['sorted_positions'][2].person.slug, 'person1')
        self.assertEqual(context1['sorted_positions'][3].person.slug, 'person2')
        self.assertEqual(context1['sorted_positions'][4].person.slug, 'person3')
        self.assertEqual(context2['sorted_positions'][0].person.slug, 'person4')
        self.assertEqual(context2['sorted_positions'][1].person.slug, 'person5')


@attr(country='south_africa')
class SAOrganisationPeopleSubPageTest(TestCase):

    def setUp(self):
        org_kind_party = models.OrganisationKind.objects.create(name='Party', slug='party')
        org_kind_parliament = models.OrganisationKind.objects.create(name='Parliament', slug='parliament')

        ncop = models.Organisation.objects.create(name='NCOP', slug='ncop', kind=org_kind_parliament)

        whip = models.PositionTitle.objects.create(name='Whip', slug='whip')
        delegate = models.PositionTitle.objects.create(name='Delegate', slug='delegate')

        aardvark = models.Person.objects.create(legal_name='Anthony Aardvark', slug='aaardvark')
        alice = models.Person.objects.create(legal_name='Alice Smith', slug='asmith')
        bob = models.Person.objects.create(legal_name='Bob Smith', slug='bsmith')
        charlie = models.Person.objects.create(legal_name='Charlie Bucket', slug='cbucket')
        zebra = models.Person.objects.create(legal_name='Zoe Zebra', slug='zzebra')
        anon = models.Person.objects.create(legal_name='', slug='anon')

        self.aardvark_ncop = aardvark_ncop= models.Position.objects.create(person=aardvark, organisation=ncop, title=delegate)
        self.alice_ncop = alice_ncop = models.Position.objects.create(person=alice, organisation=ncop, title=delegate)
        self.bob_ncop = bob_ncop = models.Position.objects.create(person=bob, organisation=ncop, title=delegate)
        self.alice_ncop_whip = alice_ncop_whip = models.Position.objects.create(person=alice, organisation=ncop, title=whip)
        self.zebra_ncop = zebra_ncop = models.Position.objects.create(person=zebra, organisation=ncop, title=delegate)
        self.anon_ncop = models.Position.objects.create(person=anon, organisation=ncop, title=delegate)

        self.charlie_ncop = models.Position.objects.create(person=charlie, organisation=ncop, title=None)

    def test_members_with_same_surname(self):
        context = self.client.get(reverse('organisation_people', kwargs={'slug': 'ncop'})).context

        expected = [
            x.id for x in
            (
                # First any positions of people with blank legal_name
                self.anon_ncop,
                # Then alphabetical order by 'surname'
                self.aardvark_ncop,
                # This should happen even if the person has a missing title
                self.charlie_ncop,
                # Inside alphabetical order, positions for the same person should be grouped
                # by person with the parliamentary membership first
                self.alice_ncop, self.alice_ncop_whip,
                self.bob_ncop,
                # Surnames beginning with Z should be at the end
                self.zebra_ncop,
                )
            ]

        self.assertEqual([x.id for x in context['sorted_positions']], expected)


@attr(country='south_africa')
class SAHansardIndexViewTest(TestCase):

    def setUp(self):
        create_sections([
            {
                'title': u"Hansard",
                'subsections': [
                    {   'title': u"2013",
                        'subsections': [
                            {   'title': u"02",
                                'subsections': [
                                    {   'title': u"16",
                                        'subsections': [
                                            {   'title': u"Proceedings of the National Assembly (2012/2/16)",
                                                'subsections': [
                                                    {   'title': u"Proceedings of Foo",
                                                        'speeches': [ 4, date(2013, 2, 16), time(9, 0) ],
                                                    },
                                                    {   'title': u"Bill on Silly Walks",
                                                        'speeches': [ 2, date(2013, 2, 16), time(12, 0) ],
                                                    },
                                                ],
                                            },
                                        ],
                                    },
                                    {
                                        'title': u"18",
                                        'subsections': [
                                            {   'title': u"Proceedings of the National Assembly (2012/2/18)",
                                                'subsections': [
                                                    {   'title': u"Budget Report",
                                                        'speeches': [ 3, date(2013, 2, 18), time(9, 0) ],
                                                    },
                                                    {   'title': u"Bill on Comedy Mustaches",
                                                        'speeches': [ 7, date(2013, 2, 18), time(12, 0) ],
                                                    },
                                                ],
                                            },
                                        ],
                                    },
                                ],
                            },
                            {
                                'title': u"Empty section",
                            }
                        ],
                    },
                ],
            },
        ])

    def test_index_page(self):
        c = Client()
        response = c.get('/hansard/')
        self.assertEqual(response.status_code, 200)

        section_name = "Proceedings of Foo"
        section = Section.objects.get(title=section_name)

        # Check that we can see the titles of sections containing speeches only
        self.assertContains(response, section_name)
        self.assertContains(response, '<a href="/%s">%s</a>' % (section.get_path, section_name), html=True)
        self.assertNotContains(response, "Empty section")

@attr(country='south_africa')
class SACommitteeIndexViewTest(WebTest):

    def setUp(self):
        self.fish_section_title = u"Oh fishy fishy fishy fishy fishy fish"
        self.forest_section_title = u"Forests are totes awesome"
        self.pmq_section_title = "Questions on 20 June 2014"
        # Make sure that the default SayIt instance exists, since when
        # testing it won't be created because of SOUTH_TESTS_MIGRATE = False
        default_instance, _ = Instance.objects.get_or_create(label='default')
        create_sections([
            {
                'title': u"Committee Minutes",
                'subsections': [
                    {   'title': u"Agriculture, Forestry and Fisheries",
                        'subsections': [
                            {   'title': u"16 November 2012",
                                'subsections': [
                                    {   'title': self.fish_section_title,
                                        'speeches': [ 7, date(2013, 2, 18), time(12, 0) ],
                                    },
                                    {
                                        'title': u"Empty section",
                                    }
                                ],
                            },
                            {   'title': "17 November 2012",
                                'subsections': [
                                    {   'title': self.forest_section_title,
                                        'speeches': [ 7, date(2013, 2, 19), time(9, 0), False ],
                                    },
                                    {
                                        'title': "Empty section",
                                    }
                                ],
                            },
                        ],
                    },
                ],
            },
            {
                'title': u"Hansard",
                'subsections': [
                    {   'title': u"Prime Minister's Questions",
                        'subsections': [
                            {   'title': self.pmq_section_title,
                                'speeches': [ 7, date(2013, 2, 18), time(12, 0) ],
                            },
                        ],
                    },
                ],
            },
        ], instance=default_instance)

    def test_committee_index_page(self):
        response = self.app.get('/committee-minutes/')
        self.assertEqual(response.status_code, 200)

        section = Section.objects.get(title=self.fish_section_title)

        # Check that we can see the titles of sections containing speeches only
        self.assertContains(response, "16 November 2012")
        self.assertContains(response, self.fish_section_title)
        self.assertContains(response,
                            '<a href="/%s">%s</a>' % (section.get_path,
                                                      self.fish_section_title),
                            html=True)
        self.assertNotContains(response, "Empty section")

    def test_committee_section_redirects(self):
        # Get the section URL:
        section = Section.objects.get(title=self.fish_section_title)
        section_url = reverse('speeches:section-view', args=(section.get_path,))
        response = self.app.get(section_url)
        self.assertEqual(response.status_code, 302)
        url_match = re.search(r'http://somewhere.or.other/\d+',
                              response.location)
        self.assertTrue(url_match)

    def view_speech_in_section(self, section_title):
        section = Section.objects.get(title=section_title)
        # Pick an arbitrary speech in that section:
        speech = Speech.objects.filter(section=section)[0]
        speech_url = reverse('speeches:speech-view', args=(speech.id,))
        # Get that URL, and expect to see a redirect to the source_url:
        return self.app.get(speech_url)

    def check_redirect(self, response):
        self.assertEqual(response.status_code, 302)
        url_match = re.search(r'http://somewhere.or.other/\d+',
                              response.location)
        self.assertTrue(url_match)

    def test_public_committee_speech_redirects(self):
        # Try a speech in a section that contains private speeches:
        self.check_redirect(self.view_speech_in_section(self.fish_section_title))

    def test_private_committee_speech_redirects(self):
        # Try a speech in a section that contains public speeches:
        self.check_redirect(self.view_speech_in_section(self.forest_section_title))

    def test_hansard_speech_returned(self):
        response = self.view_speech_in_section(self.pmq_section_title)
        self.assertEqual(response.status_code, 200)
        self.assertIn('rhubarb rhubarb', response)

@attr(country='south_africa')
class SAOrganisationDetailViewTest(WebTest):

    def setUp(self):
        # Create a test organisation and some associated models
        person = models.Person.objects.create(
            legal_name = 'Test Person',
            slug       = 'test-person',
        )

        person2 = models.Person.objects.create(
            legal_name = 'Zest ABCPerson',
            slug       = 'zest-abcperson',
        )

        organisation_kind = models.OrganisationKind.objects.create(
            name = 'Foo',
            slug = 'foo',
        )
        organisation_kind.save()

        organisation = models.Organisation.objects.create(
            name = 'Test Org',
            slug = 'test-org',
            kind = organisation_kind,
        )

        title = models.PositionTitle.objects.create(
            name = 'Test title',
            slug = 'test-title',
        )

        models.Position.objects.create(
            person = person,
            title  = title,
            organisation = organisation,
        )

        models.Position.objects.create(
            person = person2,
            title  = title,
            organisation = organisation,
        )

    def test_ordering_of_positions(self):
        # We expect the positions to be sorted by the "last name" of the
        # people in them.
        resp = self.app.get('/organisation/test-org/')
        positions = resp.context['positions']
        self.assertEqual(positions[0].person.legal_name, "Zest ABCPerson")
        self.assertEqual(positions[1].person.legal_name, "Test Person")

@attr(country='south_africa')
class FixPositionTitlesCommandTests(TestCase):
    """Test the south_africa_fix_position_title command"""

    def setUp(self):
        # Create some organisations with some people in various positions,
        # with various titles
        self.person_a = models.Person.objects.create(
            name="Person A",
            slug="person-a")
        self.person_b = models.Person.objects.create(
            name="Person B",
            slug="person-b")
        self.person_c = models.Person.objects.create(
            name="Person C",
            slug="person-c")
        self.person_d = models.Person.objects.create(
            name="Person D",
            slug="person-d")

        self.party_kind = models.OrganisationKind.objects.create(
            name="Party",
            slug="party")
        self.other_kind = models.OrganisationKind.objects.create(
            name="Other Org",
            slug="other-org")

        self.organisation_a = models.Organisation.objects.create(
            name="Organisation A",
            kind=self.party_kind,
            slug="organisation-a")
        self.organisation_b = models.Organisation.objects.create(
            name="Organisation B",
            kind=self.party_kind,
            slug="organisation-b")
        self.organisation_c = models.Organisation.objects.create(
            name="Organisation C",
            kind=self.other_kind,
            slug="organisation-c")

        self.party_member_position_title = models.PositionTitle.objects.create(
            name="Party Member",
            slug="party-member")
        self.member_position_title = models.PositionTitle.objects.create(
            name="Member",
            slug="member")
        self.other_position_title = models.PositionTitle.objects.create(
            name="Other Title",
            slug="other-title")

        self.position_a = models.Position.objects.create(
            title=self.party_member_position_title,
            person=self.person_a,
            category="other",
            organisation=self.organisation_a)
        self.position_b = models.Position.objects.create(
            title=self.party_member_position_title,
            person=self.person_b,
            category="other",
            organisation=self.organisation_b)
        self.position_c = models.Position.objects.create(
            title=self.member_position_title,
            person=self.person_c,
            category="other",
            organisation=self.organisation_a)
        self.position_d = models.Position.objects.create(
            title=self.other_position_title,
            person=self.person_d,
            category="other",
            organisation=self.organisation_b)

    def test_updates_titles_and_deletes_position(self):
        self.assertEquals(
            models.Position.objects.filter(title=self.party_member_position_title).count(),
            2)
        self.assertEquals(
            models.Position.objects.filter(title=self.member_position_title).count(),
            1)

        call_command(
            'south_africa_fix_position_titles',
            stderr=StringIO(),
            stdout=StringIO())

        # Check things are re-assigned correctly
        self.assertEquals(
            models.Position.objects.filter(title=self.party_member_position_title).count(),
            0)
        self.assertEquals(
            models.Position.objects.filter(title=self.member_position_title).count(),
            3)
        self.assertEquals(
            models.Position.objects.get(id=self.position_a.id).title,
            self.member_position_title)
        self.assertEquals(
            models.Position.objects.get(id=self.position_b.id).title,
            self.member_position_title)

        # Check that the old PositionTitle is deleted
        self.assertEqual(
            models.PositionTitle.objects.filter(name="Party Member").count(),
            0)

        # Check that nothing else got clobbered
        self.assertEquals(
            models.Position.objects.get(id=self.position_c.id).title,
            self.member_position_title)
        self.assertEquals(
            models.Position.objects.get(id=self.position_d.id).title,
            self.other_position_title)


    def test_errors_if_position_titles_not_on_parties(self):
        self.person_e = models.Person.objects.create(
            name="Person E",
            slug="person-e")
        models.Position.objects.create(
            title=self.party_member_position_title,
            person=self.person_e,
            category="other",
            organisation=self.organisation_c)

        with self.assertRaises(AssertionError):
            call_command(
                'south_africa_fix_position_titles',
                stderr=StringIO(),
                stdout=StringIO())
