from __future__ import unicode_literals, print_function, division, absolute_import

from django.contrib import admin
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
    pass
admin.site.register(Person, PersonAdmin)


class PersonInline(admin.TabularInline):
    model = Person


class CandidateAdmin(admin.ModelAdmin):
    raw_id_fields = ('person', 'race', )
    list_display = ('person', 'race', 'party', 'rating', 'is_incumbent', 'featured')
admin.site.register(Candidate, CandidateAdmin)

