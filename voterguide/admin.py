from __future__ import unicode_literals, print_function, division, absolute_import

from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ugettext as _

from .models import Election, Office, District, Race, Person, Candidate


class ElectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'election_date', 'is_active')
admin.site.register(Election, ElectionAdmin)


class OfficeAdmin(admin.ModelAdmin):
    list_display = ('name', 'priority')
admin.site.register(Office, OfficeAdmin)


class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'state', 'chamber', 'modified_on')
    search_fields = ('name', )
    list_filter = ('state', 'chamber', )

admin.site.register(District, DistrictAdmin)


def create_races_for_districts(modeladmin, request, queryset):
    for obj in queryset:
        for d in District.objects.filter(chamber=obj.office.chamber):
            Race.objects.get_or_create(election=obj.election, office=obj.office, state=obj.state, district=d)
create_races_for_districts.short_description = _("Clone to all districts")


class RaceAdmin(admin.ModelAdmin):
    list_filter = ('election', 'office', 'state', )
    search_fields = ('election__name', 'office__name', 'district__name', )
    list_display = ('election', 'office', 'district', )
    actions = [create_races_for_districts, ]
admin.site.register(Race, RaceAdmin)


class PersonAdmin(admin.ModelAdmin):
    search_fields = ('full_name', )
admin.site.register(Person, PersonAdmin)


# Candidate actions
def mark_as_winner(modeladmin, request, queryset):
    queryset.update(winner=True)
mark_as_winner.short_description = _("Mark as winner")


def copy_to_next_election(modeladmin, request, queryset):
    for obj in queryset:
        # find the next election, and create a Race object for this office/district if it doesn't already exist
        election = Election.objects.filter(election_date__gt=obj.race.election.election_date).order_by('election_date').first()
        if not election:
            modeladmin.message_user(request, _("Error: couldn't find next election. Please make sure you've added one."), level=messages.ERROR)
            continue
        new_race, created = Race.objects.get_or_create(election=election, office=obj.race.office, state=obj.race.state, district=obj.race.district)
        Candidate.objects.get_or_create(person=obj.person, race=new_race, defaults={
            'is_incumbent': obj.is_incumbent,
            'party': obj.party,
            'rating': obj.rating,
            'featured': False,
            'winner': False,
        })
copy_to_next_election.short_description = _("Copy to next election")


class CandidateAdmin(admin.ModelAdmin):
    raw_id_fields = ('person', 'race', )
    list_display = ('person', 'race', 'party', 'rating', 'is_incumbent', 'featured')
    list_filter = ('race__election', 'race__office', 'rating', 'is_incumbent', 'winner', 'party', 'featured')
    search_fields = ('person__full_name', )
    actions = [mark_as_winner, copy_to_next_election, ]
admin.site.register(Candidate, CandidateAdmin)
