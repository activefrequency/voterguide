from __future__ import unicode_literals, print_function, division, absolute_import

from django.utils.translation import ugettext as _
from django import forms

from .models import Election, Office, District, Candidate


class CandidateImportForm(forms.Form):
    election = forms.ModelChoiceField(label=_("Election"), queryset=Election.objects.all())
    winner_of_election = forms.ModelChoiceField(label=_("Mark as winner of"), queryset=Election.objects.all(), required=False)
    csv = forms.CharField(label=_("CSV"), widget=forms.Textarea(attrs={'rows': '20', 'class': 'form-control'}))


class DistrictImportForm(forms.Form):
    csv = forms.CharField(label=_("CSV"), widget=forms.Textarea(attrs={'rows': '20', 'class': 'form-control'}))


class CandidateFilterForm(forms.Form):
    """
    NB: not using django-filter here because the special cases of the "Statewide" option and Pro-Choice = "Endorsed" would be more difficult than it's worth.
    """
    office = forms.ModelChoiceField(label=_("Office"), required=False, queryset=Office.objects.all(), empty_label=_(" - ANY - "))
    party = forms.ChoiceField(label=_("Party"), required=False, choices=((('', _(" - ANY - ")),) + Candidate.PARTY_CHOICES) )
    # 'Pro' should include 'Endorsed' - handle in the view
    rating = forms.ChoiceField(label=_("Pro-Choice Rating"), required=False, choices=((('', _(" - ANY - ")),) + Candidate.RATING_CHOICES) )
    # only races with endorsements
    with_endorsements = forms.BooleanField(label=_("Only show races with endorsements"), required=False)

    def __init__(self, *args, **kwargs):
        super(CandidateFilterForm, self).__init__(*args, **kwargs)
        # add special "Statewide" option
        self.fields['district'] = forms.ChoiceField(label=_("District"), required=False, choices=([('', _(" - ANY - ")), ('S', _("Statewide")), ] + [(d.id, d) for d in District.objects.all()]))
        active_ratings = [r[0] for r in Candidate.objects.all().order_by('-rating').distinct('rating').values_list('rating')]
        choices_dict = dict(Candidate.RATING_CHOICES)
        self.fields['rating'].choices = [('', _(" - ANY - ")),] + [(r, choices_dict[r]) for r in active_ratings]

