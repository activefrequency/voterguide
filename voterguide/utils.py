from __future__ import unicode_literals, print_function, division, absolute_import

from .models import ORDINALS

from titlecase import titlecase


def normalize_ordinals(name):
    """
    Change 'Eighth Plymouth' to '8th Plymouth'
    """
    for key, val in ORDINALS.items():
        # split words, to make sure that 'fifth' doesn't match 'thirty-fifth'
        if key in name.lower().split(' '):
            name = titlecase(name.lower().replace(key, val[1]))
    return name
