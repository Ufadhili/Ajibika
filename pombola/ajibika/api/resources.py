from pombola.core.models import Place, Person, Position, PlaceKind, Organisation, PositionTitle
from tastypie import fields
from tastypie.serializers import Serializer
from tastypie.authentication import BasicAuthentication
from django.contrib.auth.models import User
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.utils import trailing_slash
from tastypie.cache import SimpleCache
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from django.conf.urls import patterns, url, include
from django.core import serializers


class PersonResource(ModelResource):
	# position = fields.ForeignKey('ajibika.api.PositionResource', full=True, null=True, blank=True)
	class Meta:
		queryset = Person.objects.all()
		default_format = "application/json"
		resource_name = 'person'
		authorization = DjangoAuthorization()
		limit = 0
		list_allowed_methods = ["get"]
		detail_allowed_methods = ["get"]
		excludes = ["summary", "biography", "honorific_prefix","honorific_suffix"]

class OrganisationResource(ModelResource):
	class Meta:
		queryset = PlaceKind.objects.all()
		default_format = "application/json"
		resource_name = 'placekind'
		authorization = DjangoAuthorization()
		limit = 0
		list_allowed_methods = ["get"]
		detail_allowed_methods = ["get"]
		excludes = ["summary", "biography", "honorific_prefix","honorific_suffix"]
		
class PlaceKindResource(ModelResource):
	class Meta:
		queryset = PlaceKind.objects.all()
		default_format = "application/json"
		resource_name = 'placekind'
		authorization = DjangoAuthorization()
		limit = 0
		list_allowed_methods = ["get"]
		detail_allowed_methods = ["get"]
		excludes = ["summary", "biography", "honorific_prefix","honorific_suffix"]


class CountyResource(ModelResource):
	# kind = fields.ForeignKey(PlaceKindResource, 'kind', full=True)
	# Organisation = fields.ForeignKey(OrganisationResource, 'Organisation', full=True, null=True, blank=True)
	class Meta:
		queryset = Place.objects.filter(kind__slug='county')
		default_format = "application/json"
		resource_name = 'county'
		authorization = DjangoAuthorization()
		limit = 0
		list_allowed_methods = ["get"]
		detail_allowed_methods = ["get"]
		include_absolute_url = True
		filtering = {
	        'slug': ALL,	        
	        'name': ALL,
        }
		excludes = ["summary"]

	
	def dehydrate(self, bundle):		
		# bundle.data["people"] = build_place_people_dict(bundle.obj.all_related_positions())
		bundle.data["county_people_uri"] = "%speople/" %(bundle.data["resource_uri"])
		bundle.data["county_projects_uri"] = "%sprojects/" %(bundle.data["resource_uri"])
		bundle.data["county_news_uri"] = "%snews/" %(bundle.data["resource_uri"])
		bundle.data["county_positions_uri"] = "%spositions/" %(bundle.data["resource_uri"])
		bundle.data["county_organisations_uri"] = "%sorganisations/" %(bundle.data["resource_uri"])
		return bundle

	def prepend_urls(self):
		return [
    	url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/people%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('people'), name="api_people"),
    	url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/projects%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('county_projects'), name="api_county_projects"),
    	url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/news%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('county_news'), name="api_county_news"),
    	url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/positions%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('positions_in_a_county'), name="api_county_positions"),
    	url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/organisations%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('organisations_in_a_county'), name="api_county_organisations"),
    	url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/transcripts%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('county_transcripts'), name="api_county_transcripts"),
    	]

	def people(self, request, **kwargs):
		""" proxy for the all_related_current_politicians method """  

		#method check to avoid bad requests
		self.method_check(request, allowed=['get'])

		# create a basic bundle object for self.get_cached_obj_get.
		basic_bundle = self.build_bundle(request=request)

		county = self.cached_obj_get(
             bundle=basic_bundle,
             **self.remove_api_resource_names(kwargs))

		people = build_place_people_dict(county.all_related_positions())
		# people = [st.__dict__ for st in county.all_related_positions()]

		return self.create_response(request, people)

	def positions_in_a_county(self, request, **kwargs):
		""" Proxy for all the people in a county """
		fields_to_hide = ["_state", "sorting_end_date", "sorting_end_date_high",\
		 "sorting_start_date", "sorting_start_date_high"]
		self.method_check(request, allowed=['get'])
		basic_bundle = self.build_bundle(request=request)
		county = self.cached_obj_get(
			bundle=basic_bundle,
			**self.remove_api_resource_names(kwargs))
		positions = [st.__dict__ for st in county.all_related_positions()]
		for org in positions:
			position =[st.__dict__ for st in PositionTitle.objects.filter(id=org["title_id"])]
			org['title'] = position[0]['name']
			for field in fields_to_hide:
				org.pop(field)

		return self.create_response(request, positions)

	def organisations_in_a_county(self, request, **kwargs):
		fields_to_hide = ["_summary_rendered", "_state", "summary", "created", "ended", "kind_id"]
		self.method_check(request, allowed=['get'])
		basic_bundle = self.build_bundle(request=request)
		county = self.cached_obj_get(
			bundle=basic_bundle,
			**self.remove_api_resource_names(kwargs))
		organisations = []
		ids = []
		people = [st.__dict__ for st in county.all_related_positions()]
		for person in people:
			ids.append(person['organisation_id'])

		unique_ids = set(ids)
		for x in unique_ids:			
			org = [st.__dict__ for st in Organisation.objects.filter(id=x)][0]
			for field in fields_to_hide:
				org.pop(field)
			organisations.append(org)

		return self.create_response(request, organisations)


"""
Pombola's Place model methods don't have a clean way of returning 
all people in a particular place so I have to hack this.

"""        
def build_place_people_dict(queryset):
	people = [st.__dict__ for st in queryset]
	fields_to_hide = ["_state","sorting_end_date",\
		"sorting_end_date_high","sorting_start_date", "sorting_start_date_high"]
	bio_fields_to_hide = ["_state","family_name","given_name","honorific_prefix","honorific_suffix",\
	"_biography_rendered","_summary_rendered","can_be_featured"]
		
	for person in people:	        	
			bio = [st.__dict__ for st in Person.objects.filter(id=person["person_id"])][0]
			for field in bio_fields_to_hide:
				bio.pop(field)

			person["personal_details"] = bio    
			org = [st.__dict__ for st in Organisation.objects.filter(id=person["organisation_id"])][0]
			# org.pop("_state")
			# person["organisation_details"] = org
			person["organisation"] = org["name"]
			# person["organisation_id"] =
			title = [st.__dict__ for st in PositionTitle.objects.filter(id=person["title_id"])][0]
			# title.pop("_state")
			# person["position_details"] = title
			person["name"] = bio["legal_name"]
			person["title"] = title["name"]
			# person["position_id"] = title["id"]
			for x in fields_to_hide:
				person.pop(x)
	return people


class PlaceResource(ModelResource):
	# politicians = fields.ToManyField('ajibika.api.PersonResource', 'all_related_current_politicians', full=True, null=True, blank=True)
	class Meta:
		# object_class = Place
		queryset = Place.objects.all()
		default_format = "application/json"
		resource_name = 'place'
		authorization = DjangoAuthorization()
		limit = 0
		list_allowed_methods = ["get"]
		detail_allowed_methods = ["get"]
		include_absolute_url = True
		filtering = {
	        'slug': ALL,	        
	        'name': ALL,
        }


	def dehydrate(self, bundle):
		# politicians = bundle.obj.all_related_current_politicians()
		# data = serializers.serialize("json", politicians)
		bundle.data["politicians"] =  bundle.obj.all_related_current_politicians()
		bundle.data["current_politician_position"] = bundle.obj.current_politician_position()
		bundle.data["related_people"] = bundle.obj.related_people()
		bundle.data["parent_places"] = bundle.obj.parent_places()
		bundle.data["related_positions"] = [st.__dict__ for st in bundle.obj.all_related_positions()]
		bundle.data["persons"] = [st.__dict__ for st in bundle.obj.all_related_current_politicians()]
		# bundle.data["senator"] = 
		# bundle.data["mcas"] = 
		# bundle.data["projects"] = 
		# bundle.data["news"] = 
		# bundle.data["governor"] = 
		# bundle.data["hansard"]
		return bundle
		
	def prepend_urls(self):		
		 return [
	            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/politicians%s$" %
	                (self._meta.resource_name, trailing_slash()),
	                self.wrap_view('all_related_current_politicians'), name="api_all_related_current_politicians"),
	        ]

	def all_related_current_politicians(self, request, **kwargs):
         """ proxy for the all_related_current_politicians method """  

         # you can do a method check to avoid bad requests
         self.method_check(request, allowed=['get'])

         # create a basic bundle object for self.get_cached_obj_get.
         basic_bundle = self.build_bundle(request=request)

         # using the primary key defined in the url, obtain the game
         place = self.cached_obj_get(
             bundle=basic_bundle,
             **self.remove_api_resource_names(kwargs))

         politicians = place.all_related_current_politicians()

         data = [st.__dict__ for st in politicians]


         return self.create_response(request, data)





class PositionResource(ModelResource):
	# person = fields.ForeignKey('ajibika.api.PersonResource', full=True, null=True, blank=True)
	class Meta:
		queryset = Position.objects.all()
		default_format = "application/json"
		resource_name = 'position'
		authorization = DjangoAuthorization()
		limit = 0
		list_allowed_methods = ["get"]
		detail_allowed_methods = ["get"]