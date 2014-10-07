from __future__ import unicode_literals, print_function, division, absolute_import

from .models import ORDINALS, NUMERALS

from titlecase import titlecase


def normalize_ordinals(name):
    """
    Change 'Eighth Plymouth' to '8th Plymouth', and '8 Plymouth' to '8th Plymouth'
    """
    # work around "SD 1"/"HD 1"
    if name.startswith("SD "):
        name = name.replace("SD ", "")
    if name.startswith("HD "):
        name = name.replace("HD ", "")

    if name.isnumeric():
        return name

    for key, val in ORDINALS.items():
        # split words, to make sure that 'fifth' doesn't match 'thirty-fifth'
        if key in name.lower().split(' '):
            name = titlecase(name.lower().replace(key, val[1]))
    for key, val in NUMERALS.items():
        # split words, to make sure that '5' doesn't match 'thirty-fifth'
        if key in name.lower().split(' '):
            name = titlecase(name.lower().replace(key, val[1]))
    # fix capitalization of "1ST", "2ND", etc"
    name = name.replace('1ST ', '1st ').replace('2ND ', '2nd ').replace('3RD ', '3rd ').replace('4TH ', '4th ').replace('5TH ', '5th ').replace('6TH ', '6th ').replace('7TH ', '7th ').replace('8TH ', '8th ').replace('9TH ', '9th ').replace('10TH ', '10th ')

    # do our best to strip extraneous spaces, inside and outside
    return name.replace('  ', ' ').replace('  ', ' ').strip()
