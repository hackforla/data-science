#!/usr/bin/env python3
"""Tests for exempt_table."""
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal

from transformations.tot_table import normalize_address_wrapper


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


#def test_address():
#    """Test address function."""
#    test_list = [
#        '5251 HOLLYWOOD BLVD',
#        '1 LMU DRIVE SUITE 2200',
#        '8405 PERSHING DRIVE UNIT 500',
#        '7310 S FIGUEROA STREET',
#        '405 East IMPERIAL HIGHWAY',
#    ]
#    test_series = pd.Series(test_list, name='STREET_ADDRESS')
#    expected_address1 = [
#        '5251 HOLLYWOOD BLVD',
#        '1 LMU DR',
#        '8405 PERSHING DR',
#        '405 E IMPERIAL HWY',
#    ]
#    expected_address2 = [
#        np.nan,
#        'STE 2200',
#        'UNIT 500',
#        np.nan,
#    ]
#    expected_frame = pd.DataFrame({
#        'Address1': expected_address1,
#        'Address2': expected_address2,
#    })
#    assert_frame_equal(address(test_series), expected_frame)
