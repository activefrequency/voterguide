from __future__ import unicode_literals, print_function, division, absolute_import

from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import MultiPolygon, Polygon, GeometryCollection
from django.conf import settings

from voterguide.models import District

import sunlight


class Command(BaseCommand):
    args = '<state>'
    help = "Import given state's districts from OpenStates API"

    def handle(self, *args, **options):
        chamber_mapping = {
            'upper': District.CHAMBER_UPPER,
            'lower': District.CHAMBER_LOWER,
        }

        # Sunlight API key is required
        sunlight.config.API_KEY = settings.SUNLIGHT_API_KEY

        for state in args:
            self.stdout.write('Importing "{}"'.format(state))

            # 'state' arguments are typically lowercased in OpenStates
            districts = sunlight.openstates.districts(state.lower())
            for d in districts:
                self.stdout.write('Importing "{}"'.format(d['name']))
                # workaround for NH and its floterial districts
                if d['boundary_id'] == 'unknown':
                    continue
                district, created = District.objects.get_or_create(openstates_boundary_id=d['boundary_id'], defaults={
                    'name': d['name'],
                    'state': state.upper(),
                    'chamber': chamber_mapping.get(d['chamber'], None),
                    'num_seats': d['num_seats'],
                    'openstates_id': d['id'],
                    'openstates_boundary_id': d['boundary_id'],
                })

                boundary = sunlight.openstates.district_boundary(d['boundary_id'])

                # most districts are only one polygon, but that's technically not guaranteed, so make sure we properly construct a MultiPolygon
                polygons = []
                for mp in boundary['shape']:
                    for p in mp:
                        polygons.append(Polygon(map(tuple, p)))
                geom = MultiPolygon(polygons)
                district.boundaries = geom

                district.save()
