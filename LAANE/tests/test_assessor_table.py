"""tests for assessor_table."""
import numpy as np
import pandas as pd
from pandas.testing import assert_series_equal

from transformations.assessor_table import (
    fractions,
    owner_names,
    special_name_assessee,
    trust_name,
)


def test_owner_names():
    """Tests the function owner_names."""
    expected_owner_names = [
        'PATEL HANISH B ALPA P',
        'ALI HOSSAN',
        'ABANILLA ALBERTO R SYLVANA R ABANILLA LIANNE M',
        'POPAL ARINA POPAL MALIHA',
    ]
    ser = pd.Series(expected_owner_names, name='Owner Names')

    first_owner_name = [
        'PATEL,HANISH B  AND ALPA P TRS',
        'ALI,HOSSAN',
        'ABANILLA,ALBERTO R AND',
        'POPAL,ARINA AND',
    ]

    df = pd.DataFrame(
        {
            'First Owner Name': first_owner_name,
            'First Owner Name Overflow': [
                'PATEL TRUST',
                '',
                'SYLVANA R AND',
                '',
            ],
            'Second Owner Name': ['', '', 'ABANILLA,LIANNE M', 'POPAL,MALIHA'],
        },
    )
    test_series = pd.Series(owner_names(df), name='Owner Names')
    assert_series_equal(test_series, ser)


def test_trust_name():
    """Test trust_name function."""
    expected_trusts = ['PATEL TRUST', '', '']
    expected_series = pd.Series(expected_trusts, name='Trust Name')
    first_owner_over = ['PATEL TRUST', '', 'SYLVANA R AND']
    df = pd.DataFrame({'First Owner Name Overflow': first_owner_over})
    test_series = pd.Series(
        trust_name(df['First Owner Name Overflow']),
        name='Trust Name',
    )
    assert_series_equal(test_series, expected_series)


def test_special_name_assessee():
    """Test special_name_assessee function."""
    expected_items = [
        'JOHN SCULL',
        'REAL ESTATE BUS GROUP-JUNE',
        'TRANSPLANT DIAGNOSTICS (TDX)',
        '',
    ]
    expected_series = pd.Series(
        expected_items,
        name='Special Name Assessee Clean',
    )
    test_special_names = [
        'C/O JOHN SCULL ',
        'REAL ESTATE BUS GROUP-JUNE',
        'C/O TRANSPLANT DIAGNOSTICS (TDX)',
        '',
    ]
    special_name_series = pd.Series(
        test_special_names,
        name='Special Name Assessee',
    )
    test_series = pd.Series(
        special_name_assessee(special_name_series),
        name='Special Name Assessee Clean',
    )
    assert_series_equal(test_series, expected_series)


def test_fractions():
    """Test fraction function."""
    test_fraction_values = [
        '',
        np.nan,
        '$  ',
        '2021-01-02 00:00:00',
    ]
    test_series = pd.Series(test_fraction_values, name='Fraction')
    expected_fractions = [
        '',
        '',
        '',
        '1/2',
    ]
    expected_series = pd.Series(expected_fractions, name='Fraction Clean')
    test_series = pd.Series(fractions(test_series), name='Fraction Clean')
    assert_series_equal(test_series, expected_series)
