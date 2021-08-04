#!/usr/bin/env python3
"""Tests for mailing_table."""
import numpy as np
import pandas as pd
from pandas.testing import assert_series_equal

from keywords import states_abbreviated
from mailing_table import state


def test_state():
    """Test for state function."""
    expected_list = [
        'CA',
        np.nan,
        np.nan,
        'FL',
        np.nan,
    ]
    expected_series = pd.Series(expected_list, name='State')
    city_state = [
        'LOS ANGELES CA          ',
        'CANOGA PARK             ',
        '                        ',
        'PALM BEACH GARDENS FL   ',
        'TORONTO CANADA M6P 3S2  ',
    ]
    assessor_dateframe = pd.DataFrame({'City State': city_state})

    assert_series_equal(
        state(assessor_dateframe['City State'], states_abbreviated),
        expected_series,
    )
