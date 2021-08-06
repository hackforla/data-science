#!/usr/bin/env python3
"""
Purpose: To transform crosscheck data to be Exempt Table compatible.

Author : Albert Ulysses <albertulysseschavez@gmail.com>
"""
from typing import Callable

import pandas as pd
from scourgify import normalize_address_record


def normalize_address_custom(address: str):
    """
    A wrapper for normalize_address_record function that prevents errors.

    :para address: an address to break into address1 and address2
    """
    try:
        return normalize_address_record(address)
    except Exception:
        return {
            'address_line_1': address,
            'address_line_2': None,
            'city': None,
            'state': None,
            'postal_code': None,
        }


def address(
    street_address: pd.Series,
    normalize_address_function: Callable,
) -> pd.DataFrame:
    """
    Transforms an address column into a dataframe of address1 and address2.

    :param street_address: A raw TOT column.
    :param normalize_address_function:
        A function that returns a dict of normalized address.
    """
    #TODO: work on this function
    address = pd.DataFrame([normalize_address_function(address) for address in street_address.tolist()], columns=['Address1', 'Address2'])
    return address[['Address1', 'Address2']]
