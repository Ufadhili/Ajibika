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
from pombola.ajibika_resources.models import (
	Video as AjibikaVideo,
	Image as AjibikaImage,
	Partner as AjibikaPartner, 
	AboutAjibika,
	Document as AjibikaDocument
	)


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

class AjibikaResource(ModelResource):
	class Meta:
		queryset = AboutAjibika.objects.all()
		default_format = "application/json"
		resource_name = "ajibika"
		limit = 0
		list_allowed_methods = ["get"]
		detail_allowed_methods = ["get"]

	def dehydrate(self, bundle):
		bundle.data["documents"] = [st.__dict__ for st in AjibikaDocument.objects.all()]
		bundle.data['images']  = [st.__dict__ for st in AjibikaImage.objects.all()]
		bundle.data['videos']   = [st.__dict__ for st in AjibikaVideo.objects.all()]
		return bundle

		
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
		bundle.data["county_documents_uri"] = "%sdocuments/" %(bundle.data["resource_uri"])
		# bundle.data["county_bills_uri"] = "%sbills/" %(bundle.data["resource_uri"])
		# bundle.data["county_transcripts_uri"] = "%stranscripts/" %(bundle.data["resource_uri"])
		# bundle.data["county_budgets_uri"] = "%sbudgets/" %(bundle.data["resource_uri"])
		# bundle.data["county_otherdocs_uri"] = "%sotherdocs/" %(bundle.data["resource_uri"])
		bundle.data["county_gallery_uri"] = "%sgallery/" %(bundle.data["resource_uri"])
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
    	url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/documents%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('county_documents'), name="api_county_documents"),
    	url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/gallery%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('county_gallery'), name="api_county_gallery"),
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
		# people = county.all_related_current_politicians()
		# people = [st.__dict__ for st in county.all_related_current_politicians()]

		return self.create_response(request, people)
	"""
	{
category: "political",
created: "2014-05-26T12:28:50.032310",
end_date: "future",
id: 1,
name: "Cornel A. Rasanga",
note: "",
organisation: "County Executive",
organisation_id: 4,
person_id: 11,
personal_details: {
	additional_name: "",
	biography: "",
	created: "2014-05-26T12:28:47.789738",
	date_of_birth: null,
	date_of_death: "future",
	email: "",
	gender: "male",
	id: 11,
	legal_name: "Cornel A. Rasanga",
	national_identity: "",
	slug: "cornel-rasanga",
	sort_name: "Rasanga",
	summary: "",
	title: "Hon.",
updated: "2014-05-26T12:28:47.789797"
},
place_id: 1,
start_date: "April 2013",
subtitle: "",
title: "Governor",
title_id: 1,
updated: "2014-05-26T12:28:50.032372"
},
	"""

	def county_projects(self, request, **kwargs):
		self.method_check(request, allowed=['get'])
		basic_bundle = self.build_bundle(request=request)
		county = self.cached_obj_get(
			bundle=basic_bundle,
			**self.remove_api_resource_names(kwargs))
		# projects = [st.__dict__ for st in county.project_set.all()]
		projects = county.project_set.all()
		project_data = []
		for project in projects:
			data = {}
			data['project_name'] = project.project_name
			data['contractor'] = project.contractor
			data['first_funding_year'] = project.first_funding_year
			data['status'] = project.project_status()
			data['location_name'] = project.location_name			
			data['absolute_url'] = project.get_absolute_url()
			data['summary'] = project.summary
			data['estimated_cost'] = project.estimated_cost
			data['sector'] = project.sector
			data['id'] = project.id

			if project.has_images():
				images = project.images.all()
				if images:
					image = images[0].image.url
					data['image'] = image
				else:
					data['image'] = None
			else:
				data['image'] = None

			# data['images'] = [st.__dict__ for st in project.images.all()]
			project_data.append(data)

			"""
			contractor: "miguna",
			county_id: 1,
			created: "2014-07-07T12:05:52.705928",
			estimated_cost: 2000000,
			first_funding_year: 2013,
			id: 3,
			location_name: "omwani",
			project_name: "te st s f s s d",
			remarks: "",
			sector: "",
			slug: "te-st-s-f-s-s-d",
			status: "POG",
			summary: "",
			total_cost: 20000000,
			updated: "2014-07-10T16:23:40.574496"
			"""

		return self.create_response(request, project_data)

	def county_news(self, request, **kwargs):		
		self.method_check(request, allowed=['get'])
		basic_bundle = self.build_bundle(request=request)
		county = self.cached_obj_get(
			bundle=basic_bundle,
			**self.remove_api_resource_names(kwargs))
		news = [st.__dict__ for st in county.newsentry_set.all()]
		news = county.newsentry_set.all()
		news_data = []
		for entry in news:
			entry_data = {}
			images = entry.images.all()
			if images:
				entry_data['image'] = images[0].image.url
			else:
				entry_data['image'] = None
				
			entry_data['title'] = entry.title
			entry_data['detail_url'] = entry.detail_url
			entry_data['title'] = entry.title
			entry_data["id"] = entry.id
			entry_data['message'] = entry.message
			entry_data['publication_date'] = entry.publication_date
			entry_data['absolute_url'] = entry.get_absolute_url()			
			news_data.append(entry_data)
		return self.create_response(request, news_data)
	
	def county_documents(self, request, **kwargs):
		COUNTY_DOCUMENT_CHOICES = {	
					'Bill':'CBL'  ,
					'Budget':'CBT',
					'Plan':'CPN' ,
					'Transcript':'CTT', 
					'Project':'CPR',
					 'Other':'COR'
			}

		self.method_check(request, allowed=['get'])
		arg = request.GET['type']
		doc_type = COUNTY_DOCUMENT_CHOICES[arg.capitalize()]
		basic_bundle = self.build_bundle(request=request)
		county = self.cached_obj_get(
			bundle=basic_bundle,
			**self.remove_api_resource_names(kwargs))
		docs = [st.__dict__ for st in county.document_set.filter(document_type=doc_type)]		
		return self.create_response(request, docs)

	def county_gallery(self, request, **kwargs):
		basic_bundle = self.build_bundle(request=request)
		county = self.cached_obj_get(
			bundle=basic_bundle,
			**self.remove_api_resource_names(kwargs))
		data = {}
		data['images'] = [st.__dict__ for st in county.images.all()]
		data['videos'] = [st.__dict__ for st in county.video_set.all()]
		return self.create_response(request, data)


	"""
	county resources:
	news = county.newsentry_set.all()
	projects = county.project_set.all()
	documents = county.document_set.all() bills, transcripts,......

	"""


	def positions_in_a_county(self, request, **kwargs):
		""" Proxy for all the positions in a county """
		fields_to_hide = ["_state", "sorting_end_date", "sorting_end_date_high",\
		 "sorting_start_date", "sorting_start_date_high"]
		self.method_check(request, allowed=['get'])
		basic_bundle = self.build_bundle(request=request)
		county = self.cached_obj_get(
			bundle=basic_bundle,
			**self.remove_api_resource_names(kwargs))
		positions = [st.__dict__ for st in county.all_related_positions()]
		# for org in positions:
		# 	position =[st.__dict__ for st in PositionTitle.objects.filter(id=org["title_id"])]
		# 	org['title'] = position[0]['name']
		# 	for field in fields_to_hide:
		# 		org.pop(field)

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
	fields_to_hide = ["sorting_end_date",\
		"sorting_end_date_high","sorting_start_date", "sorting_start_date_high"]
	bio_fields_to_hide = ["family_name","given_name","honorific_prefix","honorific_suffix",\
	"_biography_rendered","_summary_rendered","can_be_featured"]
		
	for person in people:
		details = Person.objects.filter(id=person["person_id"])
		bio = [st.__dict__ for st in details][0]
		for field in bio_fields_to_hide:
			bio.pop(field)
		person["personal_details"] = bio
		person["name"] = bio["legal_name"]  
		person["absolute_url"]  = details[0].get_absolute_url()
		person["image"] = details[0].get_api_image()
		try:
			org = [st.__dict__ for st in Organisation.objects.filter(id=person["organisation_id"])][0]
			person["organisation"] = org["name"]
		except:
			person["organisation"] = None
		
		try:
			title = [st.__dict__ for st in PositionTitle.objects.filter(id=person["title_id"])][0]
			person["title"] = title["name"]
		except:
			person["title"] = None			

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