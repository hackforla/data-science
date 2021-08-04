#!/usr/bin/env python3
"""
Purpose: To transform crosscheck data to be Exempt Table compatible.

Author : Albert Ulysses <albertulysseschavez@gmail.com>
"""
from typing import Dict

import pandas as pd

from transformations.keywords import street_ending


def street_name(
    address_series: pd.Series,
    full_street_name: Dict[str, str],
) -> pd.Series:
    """
    Transforms an address column into a column with nonabbreviated street name.

    :param address_series: a raw address series that ends in a street name.
    """
    abbre_street_series = address_series.str.strip().str.rsplit(' ', 1).str[1]
    return abbre_street_series.map(full_street_name).rename('Street Name')


def address1(address_series: pd.Series) -> pd.Series:
    """
    Transforms an address column from crosscheck into an address1 column.

    :para address_series: a raw address series that ends in a street name.
    """
    full_street_ending = street_name(address_series, street_ending)
    address_beginning = address_series.str.strip().str.rsplit(' ', 1).str[0]
    no_leading_zeros = address_beginning.str.strip().str.replace(
        '^0+',
        '',
        regex=True,
    )
    return no_leading_zeros.rename('Address1').str.replace(
        r'\s+',
        ' ',
        regex=True,
    ).str.cat(
        full_street_ending,
        sep=' ',
        na_rep='',
    ).str.strip()
