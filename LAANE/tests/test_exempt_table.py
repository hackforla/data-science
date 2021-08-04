#!/usr/bin/env python3
"""Tests for exempt_table."""
import numpy as np
import pandas as pd
from pandas.testing import assert_series_equal

from transformations.keywords import street_ending
from transformations.exempt_table import address1, street_name


def test_street_name():
    """Tests streetname function."""
    expect_list = [
        'BOULEVARD',
        'STREET',
        'HIGHWAY',
        'AVENUE',
        np.nan,
    ]
    expected_series = pd.Series(expect_list, name='Street Name')
    test_address1 = [
        '10300   WILSHIRE BLVD                   ',
        '00251 S OLIVE ST                        ',
        '01129 W PACIFIC COAST HWY               ',
        '9040 ZELZAH AVE',
        '5825 W SUNSET BLVD 1-90',
    ]
    test_series = pd.Series(test_address1, name='Address')
    assert_series_equal(
        street_name(test_series, street_ending),
        expected_series,
    )


def test_leading_zeros():
    """Test leading zeros."""
    expect_list = [
        '10300 WILSHIRE BOULEVARD',
        '251 S OLIVE STREET',
        '1129 W PACIFIC COAST HIGHWAY',
        '9040 ZELZAH AVENUE',
        '5825 W SUNSET BLVD',
    ]
    expected_series = pd.Series(expect_list, name='Address1')
    test_address1 = [
        '10300   WILSHIRE BLVD                   ',
        '00251 S OLIVE ST                        ',
        '01129 W PACIFIC COAST HWY               ',
        '9040 ZELZAH AVE',
        '5825 W SUNSET BLVD 1-90',
    ]
    test_series = pd.Series(test_address1, name='Address')
    assert_series_equal(address1(test_series), expected_series)
