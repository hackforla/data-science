#!/usr/bin/env python3
"""
Purpose: To transform crosscheck data to be Exempt Table compatible.

Author : Albert Ulysses <albertulysseschavez@gmail.com>
"""
from operator import itemgetter

import pandas as pd
from returns.result import safe
from scourgify import normalize_address_record


def normalize_address_wrapper(address: str) -> dict:
    """
    A wrapper for normalize_address_record function that prevents errors.

    :para address: an address to break into address1 and address2
    """
    # TODO type hint return typed dict typehint
    return safe(normalize_address_record)(address).value_or({
        'address_line_1': address,
        'address_line_2': None,
        'city': None,
        'state': None,
        'postal_code': None,
    })


def main():
    """ Transformations for tot sheet."""
    # to return address1 and address 2
    # if read in TOT as TOT_df use line below:
    # TOT_df[['Address1','Address2']]=[itemgetter('address_line_1','address_line_2')(normalize_address_wrapper(x)) for x in TOT_df['STREET_ADDRESS'].tolist()]
    # everything else doesn't need custom functions
    pass
