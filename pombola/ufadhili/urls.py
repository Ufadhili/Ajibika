from api import PlaceResource, PersonResource
from django.conf.urls import patterns, include, url
from tastypie.api import Api



api = Api(api_name='v1')

api.register(PlaceResource())
api.register(PersonResource())

# place_resource = PlaceResource()
# person_resource = PersonResource()


urlpatterns = patterns('',
    # The normal jazz here...
    # (r'^blog/', include('myapp.urls')),
    (r'^api/', include(api.urls)),
)