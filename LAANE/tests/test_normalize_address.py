"""Tests for addresses."""
from transformations.normalize_address import normalize_address_wrapper


def test_normalize_address_wrapper():
    """Test normalize address custom"""
    address_with_address2 = '8405 PERSHING DRIVE UNIT 500'
    expected_dict = {
        'address_line_1': '8405 PERSHING DR',
        'address_line_2': 'UNIT 500',
        'city': None,
        'state': None,
        'postal_code': None,
    }
    assert normalize_address_wrapper(address_with_address2) == expected_dict

    address_without_address2 = '1 LMU DRIVE'
    expected_dict = {
        'address_line_1': '1 LMU DR',
        'address_line_2': None,
        'city': None,
        'state': None,
        'postal_code': None,
    }
    assert normalize_address_wrapper(address_without_address2) == expected_dict

    address_with_none = None
    expected_dict = {
        'address_line_1': None,
        'address_line_2': None,
        'city': None,
        'state': None,
        'postal_code': None,
    }
    assert normalize_address_wrapper(address_with_none) == expected_dict

    address_with_error = '1 WORLD TRADE CENTER FLOOR 24'
    expected_dict = {
        'address_line_1': '1 WORLD TRADE CENTER FLOOR 24',
        'address_line_2': None,
        'city': None,
        'state': None,
        'postal_code': None,
    }

    assert normalize_address_wrapper(address_with_error) == expected_dict

    address_with_exempt = '08405 PERSHING DRIVE UNIT 500'
    expected_dict = {
        'address_line_1': '8405 PERSHING DR',
        'address_line_2': 'UNIT 500',
        'city': None,
        'state': None,
        'postal_code': None,
    }
    assert normalize_address_wrapper(address_with_address2) == expected_dict
