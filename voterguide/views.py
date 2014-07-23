from django.shortcuts import render
from django.http import Http404
from django.contrib.gis.geos import Point, GEOSGeometry

from .models import District


def home(request):
    # TODO: Google API key
    return render(request, "voterguide/home.html", {})


def district_lookup(request):
    lat = request.GET.get('lat', None)
    lng = request.GET.get('lng', None)
    
    # TODO: nicer error
    if not (lat and lng):
        raise Http404("Lat/lng required")

    # pnt = Point(float(lng), float(lat))

    # srid
    pnt = GEOSGeometry('POINT({} {})'.format(lng, lat))
    districts = District.objects.filter(boundaries__contains=pnt)

    # TODO: nicer error
    if districts.count() == 0:
        raise Http404("No results.")

    # TODO: log this - we really shouldn't have more than two (House + Senate)
    if districts.count() > 2:
        raise Http404("Found more than one district.")

    return render(request, "voterguide/district.html", {
        'districts': districts,
    })
