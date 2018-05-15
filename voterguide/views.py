from __future__ import unicode_literals, print_function, division, absolute_import
from functools import wraps

from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from django.utils.decorators import available_attrs

from .models import District, Office, Race, Election, Person, Candidate
from .forms import CandidateImportForm, DistrictImportForm, CandidateFilterForm
from .utils import normalize_ordinals

import StringIO
import unicodecsv


def placeholder_if_on(view_func):
    """
    Decorator to force a placeholder if placeholder mode is on
    and a non-logged-in user hits the site.
    """
    @wraps(view_func, assigned=available_attrs(view_func))
    def _wrapped_view(request, *args, **kwargs):
        if settings.SHOW_PLACEHOLDER and not (request.user.is_authenticated() and request.user.is_staff):
            return placeholder(request)
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def placeholder(request):
    """
    Placeholder page while primary results are switched to general.
    """
    return render(request, "voterguide/placeholder.html", {

    })


@placeholder_if_on
def home(request):
    current_election = Election.objects.filter(is_active=True).first()
    if current_election:
        featured = Candidate.objects.filter(race__election=current_election, featured=True).order_by('?').select_related('person').first()

    return render(request, "voterguide/home.html", {
        'active_page': 'home',
        'featured': featured,
    })


@placeholder_if_on
def statewide(request):
    current_election = Election.objects.get(is_active=True)
    candidates = Candidate.objects.filter(race__election=current_election, race__district=None).select_related('person', 'race', 'race__office', 'race__district').order_by(
        'race__state', 'race__election', 'race__office', 'race__district', '-is_endorsed', '-is_pro', '-is_incumbent', 'person__last_name', 'person__first_name')

    return render(request, "voterguide/statewide.html", {
        'active_page': 'statewide',
        'candidates': candidates,
    })


@placeholder_if_on
def about(request):
    return render(request, "voterguide/about.html", {
        'active_page': 'about',
    })


@placeholder_if_on
def district_lookup(request):
    lat = request.GET.get('lat', None)
    lng = request.GET.get('lng', None)
    county = request.GET.get('county', None)
    city = request.GET.get('city', None)
    address = request.GET.get('address', '')
    postal_code = request.GET.get('postal_code', '')

    # TODO: throw nicer error here if current elections <> 1
    current_election = Election.objects.get(is_active=True)

    # only show 'statewide endorsements' header if there are ANY statewide endorsed candidates
    show_endorsements = Race.objects.filter(district=None, has_endorsement=True).exists()

    if not (lat and lng):
        return render(request, "voterguide/district.html", {
            'show_endorsements': show_endorsements,
            'form_error': None,
            'address': '',
            'active_page': 'local',
        })

    # get point/districts
    pnt = GEOSGeometry('POINT({} {})'.format(lng, lat))

    district_conditions = Q(boundaries__contains=pnt)

    # if there's a postal code, find if it maps to specific districts and use those
    if postal_code:
        district_conditions = Q(district_conditions | Q(postal_code_override__contains=postal_code))

    districts = District.objects.filter(district_conditions)

    # TODO: nicer error
    if districts.count() == 0:
        return render(request, "voterguide/district.html", {
            'show_endorsements': show_endorsements,
            'form_error': 'lookup_error',
            'address': address,
            'active_page': 'local',
        })

    # TODO: log this - we really shouldn't have more than two (House + Senate)
    # ...except with Seattle City Council we definitely could.
    # if districts.count() > 2:
    #     raise Http404("Found more than one district.")

    conditions = Q(race__district__in=districts) | Q(race__district__floterial_to__in=districts)
    if county:
        conditions = Q(conditions | Q(race__district__county=county))
    if city:
        conditions = Q(conditions | Q(race__district__city=city))

    # show statewide candidates as well
    conditions = Q(conditions | Q(race__district__isnull=True))

    candidates = Candidate.objects.filter(race__election=current_election).filter(conditions).distinct().select_related('person', 'race', 'race__office', 'race__district').order_by(
        'race__state', 'race__election', 'race__office', 'race__district', '-is_incumbent', 'person__last_name', 'person__first_name')

    return render(request, "voterguide/district.html", {
        'form_error': None,
        'address': address,
        'coords': {'lat': lat, 'lng': lng},
        'districts': districts,
        'candidates': candidates,
        'show_endorsements': show_endorsements,
        'active_page': 'local',
    })


@placeholder_if_on
def candidate_list(request):
    current_election = Election.objects.get(is_active=True)
    candidates = Candidate.objects.filter(race__election=current_election).select_related('person', 'race', 'race__office', 'race__district').order_by(
        'race__state', 'race__election', 'race__office', 'race__district', '-is_endorsed', '-is_pro', '-is_incumbent', 'person__last_name', 'person__first_name')

    candidate_filter = CandidateFilterForm(request.GET, label_suffix="")
    if not candidate_filter.is_valid():
        # this shouldn't happen, but bots sometimes trigger it, so don't throw an error
        # raise Exception("candidate_filter not valid - this shouldn't happen")
        pass

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

    # only show 'endorsements' checkbox if there are ANY endorsed candidates
    show_endorsements = Race.objects.filter(has_endorsement=True).exists()
    # let setting override whether or not there are endorsements
    if not settings.VOTERGUIDE_SETTINGS.get('SHOW_ENDORSEMENTS', False):
        show_endorsements = False

    return render(request, "voterguide/candidate_list.html", {
        'candidates': candidates,
        'candidate_filter': candidate_filter,
        'show_endorsements': show_endorsements,
        'active_page': 'candidate_list',
    })


@login_required
def import_candidates(request):
    """
    Admin tool to import candidates.
    """
    # ratings inverse lookup
    rating_dict = dict([(el[1].lower(), el[0]) for el in Candidate.RATING_CHOICES])

    if request.method == "POST":
        form = CandidateImportForm(request.POST)
        if form.is_valid():
            election = form.cleaned_data.get('election')
            state = election.state
            winner_of_election = form.cleaned_data.get('winner_of_election')
            data = form.cleaned_data.get('csv')
            f = StringIO.StringIO(data)
            reader = unicodecsv.DictReader(f, encoding='utf-8', fieldnames=['Office', 'Geography', 'District', 'Priority', 'Status', 'FirstName', 'LastName', 'Party', 'Rating', 'Incumbent', 'Endorsed'])

            # Candidate For,District,Priority,Status,First,Last,Party,Rating,Incumbent?,Voted to Endorse?
            # State Representative,6th Hampden,4,Contested,Michael,Finn,D,Unknown,Yes,

            num_imported = 0
            for row in reader:
                # Look up Office
                if row['Office'].strip() in ['State Representative', 'State House']:
                    office = Office.objects.get(chamber=District.CHAMBER_LOWER)
                    chamber = District.CHAMBER_LOWER
                elif row['Office'].strip() in ['State Senate', 'State Senator']:
                    office = Office.objects.get(chamber=District.CHAMBER_UPPER)
                    chamber = District.CHAMBER_UPPER
                elif row['Office'].strip() in ['US Senate', 'US Senator']:
                    office = Office.objects.get(chamber=District.CHAMBER_USSENATE)
                    chamber = District.CHAMBER_USSENATE
                elif row['Office'].strip() in ['US Representative', 'US House']:
                    office = Office.objects.get(chamber=District.CHAMBER_USHOUSE)
                    chamber = District.CHAMBER_USHOUSE
                else:
                    try:
                        office = Office.objects.get(name=row['Office'].strip())
                        chamber = None
                    except:
                        messages.error(request, _("Couldn't find office: %(office)s" % {'office': row['Office']}))
                        continue

                # Look up district
                district_name = row['District'].strip()
                if district_name == 'Statewide' or district_name == '':
                    district = None
                else:
                    # ex: Bellingham City Council Ward 3
                    # ex: Spokane Mayor
                    # ex: Snohomish County Council District 1
                    # ex: Snohomish County Executive
                    if district_name == 'N/A':
                        if row['Office'] == 'County Executive':
                            district_name = row['Geography'].strip()
                        else:
                            district_name = "{} {}".format(row['Geography'].strip(), row['Office'].strip())
                    else:
                        district_name = "{} {} {}".format(row['Geography'].strip(), row['Office'].strip(), row['District'].strip())

                    # first, try it as-is; then try replacing ordinals
                    district_name = district_name.replace('  ', ' ').replace('  ', ' ').strip()
                    district_name = district_name.replace('County County', 'County')
                    try:
                        if chamber in [District.CHAMBER_UPPER, District.CHAMBER_LOWER]:
                            district = District.objects.get(name=row['District'].strip(), chamber=chamber, state=state)
                        elif chamber == District.CHAMBER_USHOUSE:
                            district_name = 'Congressional District {}'.format(row['District'].strip())
                            district = District.objects.get(name=district_name, chamber=chamber, state=state)
                        else:
                            if 'county' in district_name.lower():
                                chamber = District.CHAMBER_COUNTY
                            else:
                                chamber = District.CHAMBER_CITY
                            district = District.objects.get(name=district_name, chamber=chamber, state=state)
                    except District.DoesNotExist:
                        try:
                            district = District.objects.get(name=normalize_ordinals(district_name), chamber=chamber, state=state)
                        except District.DoesNotExist:
                            messages.error(request, _("Couldn't find district: %(district)s" % {'district': district_name}))
                            continue

                # Find or create race
                race, created = Race.objects.get_or_create(election=election, office=office, state=state, district=district)

                if winner_of_election:
                    try:
                        winner_of_race = Race.objects.get(election=winner_of_election, office=office, state=state, district=district)
                    except Race.DoesNotExist:
                        winner_of_race = None
                else:
                    winner_of_race = None

                # party - sort out common (non-)abbreviations
                party = row['Party'].strip().upper()
                if party == 'DEMOCRATIC':
                    party = 'D'
                elif party == 'DEMOCRAT':
                    party = 'D'
                elif party == 'DEM':
                    party = 'D'
                elif party == 'REPUBLICAN':
                    party = 'R'
                elif party == 'REP':
                    party = 'R'
                elif party == 'INDEPENDENT':
                    party = 'I'
                elif party == 'IND':
                    party = 'I'
                elif party == 'LIBERTARIAN':
                    party = 'L'
                elif party == 'LIB':
                    party = 'L'
                elif party == 'UNAFFILIATED':
                    party = 'N'
                elif party == 'UNA':
                    party = 'N'
                elif party == 'GREEN':
                    party = 'G'
                elif party == 'UNITED IND.':
                    party = 'U'

                # Find or create Person/Candidate
                # TODO: what about people with same first/last name? Need to check for district, too...
                person, created = Person.objects.get_or_create(first_name=row['FirstName'].strip(), last_name=row['LastName'].strip())
                # For now, at least note the "same-name" people, so we can check them manually
                if not created:
                    messages.info(request, _("Candidate name match: %(first_name)s %(last_name)s" % {'first_name': row['FirstName'].strip(), 'last_name': row['LastName'].strip()}))

                rating = row['Rating'].strip().upper()
                if rating == 'ANTI':
                    rating = Candidate.RATING_ANTI
                elif rating == 'PRO':
                    rating = Candidate.RATING_PRO
                elif rating == 'MIXED':
                    rating = Candidate.RATING_MIXED
                elif rating == 'RECOMMENDED':
                    rating = Candidate.RATING_RECOMMENDED
                elif rating == 'ENDORSED':
                    rating = Candidate.RATING_ENDORSED
                elif rating == 'UNKNOWN':
                    rating = Candidate.RATING_UNKNOWN
                else:
                    rating = rating_dict.get(row['Rating'].lower(), Candidate.RATING_UNKNOWN)

                endorsed_rating = row.get('Endorsed', '') or ''
                if endorsed_rating.strip().upper().find("Y") != -1:
                    rating = Candidate.RATING_ENDORSED
                values = {
                    'is_incumbent': row['Incumbent'].strip().upper().find("Y") != -1,
                    'party': party,
                    'rating': rating,
                    'featured': False,
                    'winner': False,
                }
                candidate, created = Candidate.objects.update_or_create(person=person, race=race, defaults=values)

                # if the person was in a prior race, mark them as the winner
                if winner_of_race:
                    Candidate.objects.filter(person=person, race=winner_of_race).update(winner=True)

                # Keep the count
                num_imported += 1

            # Assuming we got any, show a success message
            messages.success(request, _("%(num_imported)s rows imported!" % {'num_imported': num_imported}))
    else:
        form = CandidateImportForm()
    return render(request, "voterguide/import_candidates.html", {
        'form': form,
    })


@login_required
def import_districts(request):
    """
    Admin tool to import (floterial) districts.
    """
    if request.method == "POST":
        form = DistrictImportForm(request.POST)
        if form.is_valid():
            state = settings.VOTERGUIDE_SETTINGS.get('DEFAULT_STATE')
            data = form.cleaned_data.get('csv')
            f = StringIO.StringIO(data)
            reader = unicodecsv.DictReader(f, encoding='utf-8', fieldnames=['District', 'FloterialTo', 'Office'])

            num_imported = 0
            for row in reader:
                # Look up Office
                if row['Office'].strip() in ['State Representative', 'State House']:
                    office = Office.objects.get(chamber=District.CHAMBER_LOWER)
                    chamber = District.CHAMBER_LOWER
                elif row['Office'].strip() in ['State Senate', 'State Senator']:
                    office = Office.objects.get(chamber=District.CHAMBER_UPPER)
                    chamber = District.CHAMBER_UPPER
                else:
                    try:
                        office = Office.objects.get(name=row['Office'].strip())
                    except:
                        messages.error(request, _("Couldn't find office: %(office)s" % {'office': row['Office']}))
                        continue

                # Look up district
                target_district_name = row['FloterialTo'].strip()
                try:
                    target_district = District.objects.get(name=target_district_name, chamber=chamber, state=state)
                except District.DoesNotExist:
                    messages.error(request, _("Couldn't find district: %(district)s" % {'district': row['FloterialTo']}))
                    continue

                district_name = row['District'].strip()
                values = {
                    'is_floterial': True,
                    'state': state.upper(),
                    'chamber': chamber,
                    'num_seats': 1,
                }
                district, created = District.objects.get_or_create(name=district_name, defaults=values)
                district.floterial_to.add(target_district)
                district.save()
                num_imported += 1

            # Assuming we got any, show a success message
            messages.success(request, _("%(num_imported)s rows imported!" % {'num_imported': num_imported}))
    else:
        form = DistrictImportForm()
    return render(request, "voterguide/import_districts.html", {
        'form': form,
    })


def util_trigger_500(request):
    """Test error handling"""
    assert False
