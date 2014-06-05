Ajibika API  
=========


This API is a work in progress to enable clients read/write/update data on the Ajibika platform.
For now only the read option is enabled as there is no need to enable clients write, update or delete data from ajibika.org since that is done only on the admin dashboard. 

This API only sends responses in JSON format. There is no way of getting data in other formats at the moment. Other formats can of course be added in the future if required.

Version = v1
-------


Things you can do for now


  - List all counties
  - Get all people related to a county (Governor, Senator, County Executives, MCAs.....)
  - Get other county details suchs as projects, news, 
  - 

In order to get County details, you must know the county ID.

#####Listing Counties

```javascript
/api/v1/county/schema/?format=json #County Schema
/api/v1/county/?format=json #Lists all counties
/api/v1/county/{pk}/?format=json #Get county details where {pk} is the id of the county
/api/v1/county/set/1;3/?format=json #Get a set of counties if you know their ids.
```
###Getting a list of all counties
```sh
curl -H "Accept: application/json" http://www.ajibika.org/api/v1/county/?format=json

```
####A sample response:
```json
{
meta: {
    limit: 1000,
    next: null,
    offset: 0,
    previous: null,
    total_count: 47
},
objects: [
        {
        _summary_rendered: "<p>Siaya county falls within latitudes 0Â° 26'North to 0Â° 90' South and longitudes 33Â° 58' East and 34Â° 35' West...</p>",
        absolute_url: "/place/siaya/",
        county_news_uri: "/api/v1/county/1/news/",
        county_people_uri: "/api/v1/county/1/people/",
        county_projects_uri: "/api/v1/county/1/projects/",
        created: "2014-05-26T10:22:33.140412",
        id: 1,
        location: "POINT (34.7497558593750000 0.1400756835937500)",
        name: "Siaya",
        resource_uri: "/api/v1/county/1/",
        shape_url: "",
        slug: "siaya",
        updated: "2014-05-26T10:22:33.140447"
        },
         {
        _summary_rendered: "<p>Machakos county falls within ...</p>",
        absolute_url: "/place/machakos/",
        county_news_uri: "/api/v1/county/2/news/",
        county_people_uri: "/api/v1/county/2/people/",
        county_projects_uri: "/api/v1/county/2/projects/",
        created: "2014-05-26T10:22:33.140412",
        id: 2,
        location: "POINT (34.7497558593750000 0.1400756835937500)",
        name: "Machakos",
        resource_uri: "/api/v1/county/2/",
        shape_url: "",
        slug: "machakos",
        updated: "2014-05-26T10:22:33.140447"
],{...}
}
```
The _resource_uri_ is the county endpiont. For example based on the above response,
we can go ahead and query for details about siaya county only by sending a **GET** request to the county's _resource_uri_ which is _/api/v1/county/1/_

```sh
curl -H "Accept: application/json" http://www.ajibika.org/api/v1/county/1/?format=json

```
####Sample Response for a County endpoint
```json
{
    _summary_rendered: "<p>Siaya county falls within latitudes 0Â° 26'North to 0Â° 90' South and longitudes 33Â° 58' East and 34Â° 35' West........</p>",
    absolute_url: "/place/siaya/",
    county_news_uri: "/api/v1/county/1/news/",
    county_people_uri: "/api/v1/county/1/people/",
    county_projects_uri: "/api/v1/county/1/projects/",
    created: "2014-05-26T10:22:33.140412",
    id: 1,
    location: "POINT (34.7497558593750000 0.1400756835937500)",
    name: "Siaya",
    resource_uri: "/api/v1/county/1/",
    shape_url: "",
    slug: "siaya",
    updated: "2014-05-26T10:22:33.140447"
}
```
You can get more details about a County by following the respective endpoints for county news, county people, county projects.......

####Lets get all the people associated with Siaya County whose id is 1.
```sh
curl -H "Accept: application/json" http://www.ajibika.org/api/v1/county/1/people/?format=json
```
####Sample response for People associated with Siaya County

```json
    [{
        category: "political",
        created: "2014-05-27T15:51:17.086624",
        end_date: "future",
        id: 2,
        name: "Obare Aloyce",
        note: "",
        organisation: "County Executive",
        organisation_details: {
            _summary_rendered: "",
            created: "2014-05-23T12:54:01.841432",
            ended: "future",
            id: 4,
            kind_id: 1,
            name: "County Executive",
            slug: "county-executive",
            started: "April 2013",
            summary: "",
            updated: "2014-05-23T12:54:01.841467"
        },
        personal_details: {
            _biography_rendered: "",
            _summary_rendered: "<p>Chief of Staff Siaya County</p>",
            additional_name: "",
            biography: "",
            can_be_featured: false,
            created: "2014-05-27T15:51:14.984178",
            date_of_birth: null,
            date_of_death: null,
            email: "",
            family_name: "",
            gender: "female",
            given_name: "",
            honorific_prefix: "",
            honorific_suffix: "",
            id: 12,
            legal_name: "Obare Aloyce",
            national_identity: "",
            slug: "obare-aloyce",
            sort_name: "Aloyce",
            summary: "Chief of Staff Siaya County",
            title: "",
            updated: "2014-05-27T15:54:52.613548"
        },
        place_id: 1,
        position: "Minister",
        position_details: {
            _summary_rendered: "<p>County Minister</p>",
            created: "2014-05-23T12:54:51.574599",
            id: 3,
            name: "Minister",
            requires_place: true,
            slug: "minister",
            summary: "County Minister",
            updated: "2014-05-23T12:54:51.574694"
            },
            start_date: "April 2013",
            subtitle: "Chief of Staff",
            title_id: 3,
            updated: "2014-05-27T15:54:52.808560"
        },
    {
        category: "political",
        created: "2014-05-26T12:28:50.032310",
        end_date: "future",
        id: 1,
        name: "Cornel A. Rasanga",
        note: "",
        organisation: "County Executive",
        organisation_details: {
        _summary_rendered: "",
            created: "2014-05-23T12:54:01.841432",
            ended: "future",
            id: 4,
            kind_id: 1,
            name: "County Executive",
            slug: "county-executive",
            started: "April 2013",
            summary: "",
            updated: "2014-05-23T12:54:01.841467"
        },
        personal_details: {
            _biography_rendered: "",
            _summary_rendered: "<p>H.E Hon. Cornel A. Rasanga is......... Hon. Rasanga has a Bachelor of Arts and a Bachelor of Law DegreesÂ from the University of Nairobi and currently is undertaking a Master of Laws Degree at the atÂ the University of Nairobi. </p>",
            additional_name: "",
            biography: "",
            can_be_featured: true,
            created: "2014-05-26T12:28:47.789738",
            date_of_birth: null,
            date_of_death: "future",
            email: "",
            family_name: "",
            gender: "male",
            given_name: "",
            honorific_prefix: "",
            honorific_suffix: "",
            id: 11,
            legal_name: "Cornel A. Rasanga",
            national_identity: "",
            slug: "cornel-rasanga",
            sort_name: "Rasanga",
            summary: "H.E Hon. Cornel A. Rasanga .......Laws Degree at the atÂ the University of Nairobi. ",
            title: "Hon.",
            updated: "2014-05-26T12:28:47.789797"
        },
        place_id: 1,
        position: "Governor",
        position_details: {
            _summary_rendered: "",
            created: "2014-05-05T14:37:17.744510",
            id: 1,
            name: "Governor",
            requires_place: true,
            slug: "governor",
            summary: "",
            updated: "2014-05-05T14:37:17.744536"
        },
        start_date: "April 2013",
        subtitle: "",
        title_id: 1,
        updated: "2014-05-26T12:28:50.032372"
        },......]
```
***Still writing ***