"""
Purpose: This is for address normalization across all dataset.

Author : Albert Ulysses <albertulysseschavez@gmail.com>
"""
from returns.result import safe
from scourgify import normalize_address_record


def normalize_address_wrapper(address: str) -> dict:
    """
    A wrapper that handles errors for normalize_address_record function.

    :param address: an address to break into multiple address fields.
    """
    # TODO Would like to have type hint return a dataclass since it's mixed data
    # default return should be empty strings and postal should be 00000.
    return safe(normalize_address_record)(address).value_or(
        {
            'address_line_1': address,
            'address_line_2': '',
            'city': '',
            'state': '',
            'postal_code': 00000,
        },
    )
