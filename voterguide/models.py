from __future__ import unicode_literals, print_function, division, absolute_import

from django.utils.translation import ugettext as _
from django.contrib.gis.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings

from titlecase import titlecase


@python_2_unicode_compatible
class Election(models.Model):
    """
    Election - i.e. '2014 General'
    """
    ELECTION_TYPE_PRIMARY = "P"
    ELECTION_TYPE_GENERAL = "G"
    ELECTION_TYPE_SPECIAL = "S"
    ELECTION_TYPE_CHOICES = (
        (ELECTION_TYPE_PRIMARY, _("Primary")),
        (ELECTION_TYPE_GENERAL, _("General")),
        (ELECTION_TYPE_SPECIAL, _("Special")),
    )

    name = models.CharField(verbose_name=_("Name"), max_length=100)
    state = models.CharField(verbose_name=_("State"), max_length=2, default=settings.VOTERGUIDE_SETTINGS['DEFAULT_STATE'])
    year = models.IntegerField(verbose_name=_("Year"), default=settings.VOTERGUIDE_SETTINGS['DEFAULT_YEAR'])
    election_type = models.CharField(verbose_name=_("Election type"), max_length=1, choices=ELECTION_TYPE_CHOICES)
    election_date = models.DateField(verbose_name=_("Election date"))
    is_active = models.BooleanField(verbose_name=_("Active"), help_text=_("Only one election at a time should be 'active' - this is what's featured on the site."))

    created_on = models.DateTimeField(verbose_name=_("Created"), auto_now_add=True, editable=False)
    modified_on = models.DateTimeField(verbose_name=_("Modified"), auto_now=True, editable=False)

    class Meta:
        verbose_name = _("Election")
        verbose_name_plural = _("Elections")
        ordering = ['-is_active', 'election_date']

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class District(models.Model):
    """
    Legislative district, i.e. 'Fourth Middlesex'
    """
    CHAMBER_UPPER = 1
    CHAMBER_LOWER = 2
    CHAMBER_COUNTY = 3
    CHAMBER_CITY = 4
    CHAMBER_CHOICES = (
        (CHAMBER_UPPER, _("State Senate")),
        (CHAMBER_LOWER, _("State House")),
        (CHAMBER_COUNTY, _("County")),
        (CHAMBER_CITY, _("City Council")),
    )

    name = models.CharField(verbose_name=_("Name"), max_length=200)
    code = models.CharField(verbose_name=_("Code"), max_length=50, blank=True, help_text=_("Sortable code, i.e. 'MID08'"))
    idx = models.IntegerField(verbose_name=_("Order"), default=0, help_text=_("Sort order; useful if sorting by district name alphabetically doesn't make sense and we don't have codes. "))
    state = models.CharField(verbose_name=_("State"), max_length=2, default=settings.VOTERGUIDE_SETTINGS['DEFAULT_STATE'])
    chamber = models.IntegerField(verbose_name=_("Chamber"), choices=CHAMBER_CHOICES)
    num_seats = models.IntegerField(verbose_name=_("# Seats"), default=1, help_text=_("Number of seats in district - typically 1"))

    openstates_id = models.CharField(verbose_name=_("OpenStates ID"), max_length=100, blank=True, null=True, help_text=_("ID from OpenStates API, e.g. 'ma-lower-Eighth Middlesex'"))
    openstates_boundary_id = models.CharField(verbose_name=_("OpenStates Boundary ID"), max_length=100, blank=True, null=True, help_text=_("Boundary ID from OpenStates API, e.g. 'sldu/ma-worcester-middlesex'"))

    # MultiPolygon rather than a GeometryCollection - the latter can't be searched effectively
    boundaries = models.MultiPolygonField(verbose_name=_("Boundaries"), blank=True, null=True)

    # county- and city-wide races
    county = models.CharField(verbose_name=_("County"), max_length=100, blank=True, null=True)
    city = models.CharField(verbose_name=_("City"), max_length=100, blank=True, null=True)

    # floterial districts
    floterial_to = models.ManyToManyField("self", blank=True, related_name="floterial_districts")
    is_floterial = models.BooleanField(default=False)

    created_on = models.DateTimeField(verbose_name=_("Created"), auto_now_add=True, editable=False)
    modified_on = models.DateTimeField(verbose_name=_("Modified"), auto_now=True, editable=False)

    # use a GeoManager in order to do geo queries
    objects = models.GeoManager()

    class Meta:
        verbose_name = _("District")
        verbose_name_plural = _("Districts")
        ordering = ['chamber', 'code', 'name', 'idx']

    def __str__(self):
        return '{} - {}'.format(self.get_chamber_display(), self.name)

    def save(self, *args, **kwargs):
        self.normalize_name()
        super(District, self).save(*args, **kwargs)

    def normalize_name(self):
        """
        The OpenStates data for some states (i.e. MA) lists district names as 'Eighth Plymouth'.
        This is harder to read and order, so instead we want it to be "Plymouth 8th" (assuming it has a number in the district name).
        Also, if it doesn't have a sortable code, make one.
        """
        name = self.name.lower()
        for key, val in ORDINALS.items():
            # split words, to make sure that 'fifth' doesn't match 'thirty-fifth'
            if key in name.split(' '):
                code = name.replace(key, '').strip().replace(',', '').replace(' ', '-').upper() + '-' + str(val[0]).zfill(3)
                name = titlecase(name.replace(key, val[1]))
                self.name = name
                self.code = code
        if not self.code:
            self.code = name.strip().replace(',', '').replace(' ', '-').upper()
        self.code = self.code.upper()
        # if a code is a digit, and doesn't start with a zero, zero-pad it
        if self.code.isdigit() and self.code[0] != '0':
            self.code = self.code.zfill(3)


@python_2_unicode_compatible
class Office(models.Model):
    """
    Office - i.e. 'Governor'
    """
    name = models.CharField(verbose_name=_("Name"), max_length=100)
    priority = models.IntegerField(verbose_name=_("Priority"), default=0, help_text=_("Higher score means it'll be listed first in a list with multiple offices."))
    chamber = models.IntegerField(verbose_name=_("Chamber"), blank=True, null=True, choices=District.CHAMBER_CHOICES, help_text=_("Optional"))

    created_on = models.DateTimeField(verbose_name=_("Created"), auto_now_add=True, editable=False)
    modified_on = models.DateTimeField(verbose_name=_("Modified"), auto_now=True, editable=False)

    class Meta:
        verbose_name = _("Office")
        verbose_name_plural = _("Offices")
        ordering = ['-priority']

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Race(models.Model):
    """
    Race - i.e. '2014 MA General - State Senate - Fourth Essex'
    """
    election = models.ForeignKey(Election)
    office = models.ForeignKey(Office)
    state = models.CharField(verbose_name=_("State"), max_length=2, default=settings.VOTERGUIDE_SETTINGS['DEFAULT_STATE'])
    district = models.ForeignKey(District, blank=True, null=True, help_text=_("Optional - blank if statewide race."))
    # Is there an endorsed candidate in this race? (Derived)
    has_endorsement = models.BooleanField(default=False, editable=False)

    created_on = models.DateTimeField(verbose_name=_("Created"), auto_now_add=True, editable=False)
    modified_on = models.DateTimeField(verbose_name=_("Modified"), auto_now=True, editable=False)

    class Meta:
        verbose_name = _("Race")
        verbose_name_plural = _("Races")
        ordering = ['state', 'election', 'office', 'district']

    def __str__(self):
        if self.district:
            return "{} - {} - {} - {}".format(self.election.name, self.state, self.office.name, self.district.name)
        else:
            return "{} - {} - {}".format(self.election.name, self.state, self.office.name)

    def save(self, *args, **kwargs):
        self.has_endorsement = self.candidate_set.filter(is_endorsed=True).exists()
        super(Race, self).save(*args, **kwargs)

    def table_label(self):
        if self.district:
            return "{} - {}".format(self.office.name, self.district.name)
        else:
            return self.office.name


@python_2_unicode_compatible
class Person(models.Model):
    full_name = models.CharField(verbose_name=_("Full name"), blank=True, max_length=100, help_text=_("How the full name should be displayed, with any punctuation."))
    first_name = models.CharField(verbose_name=_("First name"), blank=True, max_length=50)
    middle = models.CharField(verbose_name=_("Middle name"), blank=True, max_length=50)
    last_name = models.CharField(verbose_name=_("Last name"), blank=True, max_length=50)
    suffixes = models.CharField(verbose_name=_("Suffixes"), blank=True, max_length=50)
    openstates_legid = models.CharField(verbose_name=_("OpenStates ID"), blank=True, max_length=20, help_text=_("Permanent OpenStates leg_id - i.e. 'ILL000555'"))
    photo_url = models.CharField(verbose_name=_("Photo URL"), blank=True, max_length=200, help_text=_("URL to candidate photo (optional)"))
    blurb = models.TextField(verbose_name=_("Blurb"), blank=True, max_length=500, help_text=_("Blurb if featured (can contain HTML)"))

    created_on = models.DateTimeField(verbose_name=_("Created"), auto_now_add=True, editable=False)
    modified_on = models.DateTimeField(verbose_name=_("Modified"), auto_now=True, editable=False)

    class Meta:
        verbose_name = _("Person")
        verbose_name_plural = _("People")
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if not self.full_name:
            self.full_name = "{} {}".format(self.first_name, self.last_name)
        super(Person, self).save(*args, **kwargs)


@python_2_unicode_compatible
class Candidate(models.Model):
    PARTY_D = _("D")
    PARTY_G = _("G")
    PARTY_R = _("R")
    PARTY_I = _("I")
    PARTY_L = _("L")
    PARTY_U = _("U")
    PARTY_N = _("N")
    PARTY_CHOICES = (
        (PARTY_D, _("Democrat")),
        (PARTY_R, _("Republican")),
        (PARTY_I, _("Independent")),
        (PARTY_L, _("Libertarian")),
        (PARTY_G, _("Green")),
        (PARTY_U, _("United Ind.")),
        (PARTY_N, _("Unaffiliated")),
    )

    RATING_UNKNOWN = 0
    RATING_ANTI = 20
    RATING_MIXED = 40
    RATING_RECOMMENDED = 50
    RATING_PRO = 60
    RATING_ENDORSED = 100
    RATING_CHOICES = (
        (RATING_ENDORSED, _("Endorsed")),
        (RATING_PRO, _("Pro-Choice")),
        (RATING_RECOMMENDED, _("Recommended")),
        (RATING_MIXED, _("Mixed")),
        (RATING_ANTI, _("Anti-Choice")),
        (RATING_UNKNOWN, _("Unknown")),
    )

    person = models.ForeignKey(Person)
    race = models.ForeignKey(Race)

    is_incumbent = models.BooleanField(verbose_name=_("Incumbent"), default=False)
    party = models.CharField(verbose_name=_("Party"), max_length=2, choices=PARTY_CHOICES, blank=True, null=True)
    rating = models.IntegerField(verbose_name=_("Rating"), choices=RATING_CHOICES, default=RATING_UNKNOWN)
    featured = models.BooleanField(verbose_name=_("Featured"), default=False)
    winner = models.BooleanField(verbose_name=_("Winner"), default=False)
    about_blurb = models.TextField(verbose_name=_("'About' Blurb"), blank=True, max_length=500, help_text=_("Candidate Statement (can contain HTML)"))

    # derived fields to make sorting & filtering easier
    is_endorsed = models.BooleanField(verbose_name=_("Endorsed?"), default=False, editable=False)
    is_pro = models.BooleanField(verbose_name=_("Endorsed or Pro?"), default=False, editable=False)

    created_on = models.DateTimeField(verbose_name=_("Created"), auto_now_add=True, editable=False)
    modified_on = models.DateTimeField(verbose_name=_("Modified"), auto_now=True, editable=False)

    class Meta:
        verbose_name = _("Candidate")
        verbose_name_plural = _("Candidates")
        ordering = ['race__state', 'race__election', 'race__office', 'race__district', 'person__last_name', 'person__first_name']

    def __str__(self):
        return self.person.full_name

    def save(self, *args, **kwargs):
        self.is_endorsed = (self.rating == Candidate.RATING_ENDORSED)
        self.is_pro = (self.rating == Candidate.RATING_ENDORSED) or (self.rating == Candidate.RATING_PRO)
        super(Candidate, self).save(*args, **kwargs)
        # save Race to make sure that has_endorsement is up-to-date
        self.race.save()


# list of ordinals - see District.normalize_name
ORDINALS = {
    "first": (1, "1st"),
    "second": (2, "2nd"),
    "third": (3, "3rd"),
    "fourth": (4, "4th"),
    "fifth": (5, "5th"),
    "sixth": (6, "6th"),
    "seventh": (7, "7th"),
    "eighth": (8, "8th"),
    "ninth": (9, "9th"),
    "tenth": (10, "10th"),
    "eleventh": (11, "11th"),
    "twelfth": (12, "12th"),
    "thirteenth": (13, "13th"),
    "fourteenth": (14, "14th"),
    "fifteenth": (15, "15th"),
    "sixteenth": (16, "16th"),
    "seventeenth": (17, "17th"),
    "eighteenth": (18, "18th"),
    "nineteenth": (19, "19th"),
    "twentieth": (20, "20th"),
    "twenty-first": (21, "21st"),
    "twenty-second": (22, "22nd"),
    "twenty-third": (23, "23rd"),
    "twenty-fourth": (24, "24th"),
    "twenty-fifth": (25, "25th"),
    "twenty-sixth": (26, "26th"),
    "twenty-seventh": (27, "27th"),
    "twenty-eighth": (28, "28th"),
    "twenty-ninth": (29, "29th"),
    "thirtieth": (39, "30th"),
    "thirty-first": (31, "31st"),
    "thirty-second": (32, "32nd"),
    "thirty-third": (33, "33rd"),
    "thirty-fourth": (34, "34th"),
    "thirty-fifth": (35, "35th"),
    "thirty-sixth": (36, "36th"),
    "thirty-seventh": (37, "37th"),
    "thirty-eighth": (38, "38th"),
    "thirty-ninth": (39, "39th"),
    "fortieth": (40, "40th"),
}

NUMERALS = {
    "1": (1, "1st"),
    "2": (2, "2nd"),
    "3": (3, "3rd"),
    "4": (4, "4th"),
    "5": (5, "5th"),
    "6": (6, "6th"),
    "7": (7, "7th"),
    "8": (8, "8th"),
    "9": (9, "9th"),
    "10": (10, "10th"),
    "11": (11, "11th"),
    "12": (12, "12th"),
    "13": (13, "13th"),
    "14": (14, "14th"),
    "15": (15, "15th"),
    "16": (16, "16th"),
    "17": (17, "17th"),
    "18": (18, "18th"),
    "19": (19, "19th"),
    "20": (20, "20th"),
    "21": (21, "21st"),
    "22": (22, "22nd"),
    "23": (23, "23rd"),
    "24": (24, "24th"),
    "25": (25, "25th"),
    "26": (26, "26th"),
    "27": (27, "27th"),
    "28": (28, "28th"),
    "29": (29, "29th"),
    "30": (39, "30th"),
    "31": (31, "31st"),
    "32": (32, "32nd"),
    "33": (33, "33rd"),
    "34": (34, "34th"),
    "35": (35, "35th"),
    "36": (36, "36th"),
    "37": (37, "37th"),
    "38": (38, "38th"),
    "39": (39, "39th"),
    "40": (40, "40th"),
}
