"""
Purpose: To transform crosscheck data to be Exempt Table compatible.

Author : Albert Ulysses <albertulysseschavez@gmail.com>
"""
from returns.result import safe
from scourgify import normalize_address_record


def normalize_address_wrapper(address: str) -> dict:
    """
    A wrapper for normalize_address_record function that handles errors.

    :para address: an address to break into address1 and address2
    """
    # TODO Would like to have type hint return typeddict
    return safe(normalize_address_record)(address).value_or({
        'address_line_1': address,
        'address_line_2': None,
        'city': None,
        'state': None,
        'postal_code': None,
    })
