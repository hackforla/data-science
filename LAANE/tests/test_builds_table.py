"""Tests for builds_table."""
import pandas as pd
from pandas.testing import assert_frame_equal

from transformations.builds_table import builds


def test_build():
    """Test for builds function."""
    test_df = pd.DataFrame(
        {
            'BD1 Baths': [2],
            'BD1 Bedrooms': [3],
            'BD1 Square Feet': [2128],
            'BD1 Units': [2],
            'BD1 Year Built': [1963],
            'BD2 Baths': [4],
            'BD2 Bedrooms': [3],
            'BD2 Square Feet': [1500],
            'BD2 Units': [1],
            'BD2 Year Built': [1999],
        },
    )
    expected_df = pd.DataFrame(
        {
            'Baths': [2],
            'Bedrooms': [3],
            'Square Feet': [2128],
            'Units': [2],
            'Year Built': [1963],
            'Build Number': [1],
        },
    )
    assert_frame_equal(builds(test_df, 1), expected_df)
