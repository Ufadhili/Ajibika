from pygeocoder import Geocoder


def geocoder(country, q, decimal_places=3):

    components = "country:" + country
    response = Geocoder.geocode(q, components=components)

    results = []

    for entry in response.raw:

        # The Google Geocoder API will return the country used in the components if
        # there is no match. Filter this from our results.
        if "country" in entry['types']:
            continue
        
        result = {
            "address":   entry['formatted_address'],
            "latitude":  entry['geometry']['location']['lat'],
            "longitude": entry['geometry']['location']['lng'],
        }

        # round to the require precision
        for key in ['latitude','longitude']:
            result[key] = round(result[key], decimal_places)

        # Check that the result has not already been added. This is possible
        # when several different areas evaluate to the same one (eg various
        # instances of South Africa's "Cape Town").
        if result not in results:
            results.append( result )

    return results
