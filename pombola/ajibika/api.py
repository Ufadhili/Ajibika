from pombola.core.models import Place, Person, Position
from tastypie import fields
from tastypie.serializers import Serializer
from tastypie.authentication import BasicAuthentication
from django.contrib.auth.models import User
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.utils import trailing_slash
from tastypie.cache import SimpleCache
from tastypie.resources import ModelResource
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

	def dehydrate(self, bundle):
		# politicians = bundle.obj.all_related_current_politicians()
		# data = serializers.serialize("json", politicians)
		bundle.data["politicians"] =  bundle.obj.all_related_current_politicians()
		bundle.data["current_politician_position"] = bundle.obj.current_politician_position()
		bundle.data["related_people"] = bundle.obj.related_people()
		bundle.data["parent_places"] = bundle.obj.parent_places()
		bundle.data["related_positions"] = [st.__dict__ for st in bundle.obj.all_related_positions()]
		# bundle.data["persons"] = [st.__dict__ for st in bundle.obj.all_related_current_politicians()]
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
         """ proxy for the game.start method """  

         # you can do a method check to avoid bad requests
         self.method_check(request, allowed=['get'])

         # create a basic bundle object for self.get_cached_obj_get.
         basic_bundle = self.build_bundle(request=request)

         # using the primary key defined in the url, obtain the game
         place = self.cached_obj_get(
             bundle=basic_bundle,
             **self.remove_api_resource_names(kwargs))

         politicians = place.all_related_current_politicians()

         data = serializers.serialize("json", politicians)


         return self.create_response(request, data)





