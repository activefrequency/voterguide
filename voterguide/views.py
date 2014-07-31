from __future__ import unicode_literals, print_function, division, absolute_import

from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.http import Http404
from django.contrib.gis.geos import Point, GEOSGeometry
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import District, Office, Race, Election, Person, Candidate
from .forms import CandidateImportForm, CandidateFilterForm
from .utils import normalize_ordinals

import StringIO
import unicodecsv


def home(request):
    current_election = Election.objects.get(is_active=True)
    featured = Candidate.objects.filter(race__election=current_election, featured=True).order_by('?').select_related('person').first()

    return render(request, "voterguide/home.html", {
        'active_page': 'home',
        'featured': featured,
    })


def statewide(request):
    current_election = Election.objects.get(is_active=True)
    candidates = Candidate.objects.filter(race__election=current_election, race__district=None).select_related('person', 'race', 'race__office', 'race__district').order_by(
        'race__state', 'race__election', 'race__office', 'race__district', '-is_endorsed', '-is_pro', '-is_incumbent', 'person__last_name', 'person__first_name')

    return render(request, "voterguide/statewide.html", {
        'active_page': 'statewide',
        'candidates': candidates,
    })


def about(request):
    return render(request, "voterguide/about.html", {
        'active_page': 'about',
    })


def district_lookup(request):
    lat = request.GET.get('lat', None)
    lng = request.GET.get('lng', None)
    address = request.GET.get('address', '')
    
    # TODO: throw nicer error here if current elections <> 1
    current_election = Election.objects.get(is_active=True)

    statewide_endorsees = Candidate.objects.filter(race__election=current_election, race__district=None, rating=Candidate.RATING_ENDORSED).select_related('person', 'race', 'race__office').order_by(
        'race__state', 'race__election', 'race__office', '-is_endorsed', '-is_pro', '-is_incumbent', 'person__last_name', 'person__first_name')

    if not (lat and lng):
        return render(request, "voterguide/district.html", {
            'form_error': None,
            'address': '',
            'statewide_endorsees': statewide_endorsees,
            'active_page': 'local',
        })

    # get point/districts
    pnt = GEOSGeometry('POINT({} {})'.format(lng, lat))
    districts = District.objects.filter(boundaries__contains=pnt)

    # TODO: nicer error
    if districts.count() == 0:
        return render(request, "voterguide/district.html", {
            'form_error': 'lookup_error',
            'address': address,
            'statewide_endorsees': statewide_endorsees,
            'active_page': 'local',
        })

    # TODO: log this - we really shouldn't have more than two (House + Senate)
    if districts.count() > 2:
        raise Http404("Found more than one district.")

    candidates = Candidate.objects.filter(race__election=current_election, race__district__in=districts).select_related('person', 'race', 'race__office', 'race__district').order_by(
        'race__state', 'race__election', 'race__office', 'race__district', '-is_incumbent', 'person__last_name', 'person__first_name')

    return render(request, "voterguide/district.html", {
        'form_error': None,
        'address': address,
        'districts': districts,
        'candidates': candidates,
        'statewide_endorsees': statewide_endorsees,
        'active_page': 'local',
    })


def candidate_list(request):
    current_election = Election.objects.get(is_active=True)
    candidates = Candidate.objects.filter(race__election=current_election).select_related('person', 'race', 'race__office', 'race__district').order_by(
        'race__state', 'race__election', 'race__office', 'race__district', '-is_endorsed', '-is_pro', '-is_incumbent', 'person__last_name', 'person__first_name')

    candidate_filter = CandidateFilterForm(request.GET, label_suffix="")
    if not candidate_filter.is_valid():
        raise Exception("candidate_filter not valid - this shouldn't happen")

    office = candidate_filter.cleaned_data.get('office', None)
    if office:
        candidates = candidates.filter(race__office=office)

    district = candidate_filter.cleaned_data.get('district', None)
    if district:
        if district == 'S':
            district = None
        candidates = candidates.filter(race__district=district)

    party = candidate_filter.cleaned_data.get('party', None)
    if party:
        candidates = candidates.filter(party=party)

    # Special case: 'Pro' implies 'Endorsed'
    rating = candidate_filter.cleaned_data.get('rating', None)
    if rating:
        if rating == str(Candidate.RATING_PRO):
            candidates = candidates.filter(Q(rating=Candidate.RATING_PRO) | Q(rating=Candidate.RATING_ENDORSED))
        else:
            candidates = candidates.filter(rating=rating)

    # "Only races with endorsements"
    with_endorsements = candidate_filter.cleaned_data.get('with_endorsements', None)
    if with_endorsements:
        candidates = candidates.filter(race__has_endorsement=True)

    return render(request, "voterguide/candidate_list.html", {
        'candidates': candidates,
        'candidate_filter': candidate_filter,
        'active_page': 'candidate_list',
    })


@login_required
def import_candidates(request):
    """
    Admin tool to import candidates.
    """
    # ratings inverse lookup
    rating_dict = dict([(el[1], el[0]) for el in Candidate.RATING_CHOICES])

    if request.method == "POST":
        form = CandidateImportForm(request.POST)
        if form.is_valid():
            election = form.cleaned_data.get('election')
            data = form.cleaned_data.get('csv')
            f = StringIO.StringIO(data)
            reader = unicodecsv.DictReader(f, fieldnames=['Office', 'District', 'FirstName', 'LastName', 'Party', 'Rating', 'Incumbent'])

            num_imported = 0
            for row in reader:
                # Look up Office
                # TODO: this is a horrible hardcoded hack
                if row['Office'] == 'State Representative':
                    office_id = 7
                    chamber = District.CHAMBER_LOWER
                elif row['Office'] == 'State Senate':
                    office_id = 2
                    chamber = District.CHAMBER_UPPER
                else:
                    messages.error(request, _("Couldn't find office: %(office)s" % {'office': row['Office']}))
                    continue
                office = Office.objects.get(id=office_id)

                # Look up district
                try:
                    district = District.objects.get(name=normalize_ordinals(row['District']), chamber=chamber)
                except District.DoesNotExist:
                    messages.error(request, _("Couldn't find district: %(district)s" % {'district': row['District']}))
                    continue

                # Find or create race
                race, created = Race.objects.get_or_create(election=election, office=office, state=election.state, district=district)
                
                # Find or create Person/Candidate
                # TODO: what about people with same first/last name? Need to check for district, too...
                person, created = Person.objects.get_or_create(first_name=row['FirstName'], last_name=row['LastName'])
                candidate, created = Candidate.objects.get_or_create(person=person, race=race, defaults={
                    'is_incumbent': row['Incumbent'] == 'Y',
                    'party': row['Party'],
                    'rating': rating_dict[row['Rating']],
                    'featured': False,
                    'winner': False,
                })

                # Keep the count
                num_imported += 1

            # Assuming we got any, show a success message
            messages.success(request, _("%(num_imported)s rows imported!" % {'num_imported': num_imported}))
    else:
        form = CandidateImportForm()
    return render(request, "voterguide/import_candidates.html", {
        'form': form,
    })











