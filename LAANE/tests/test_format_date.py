"""Tests for format_date."""
from transformations.format_date import format_date


def test_format_date():
    """Test the function for formatdate."""
    test_list = [
        '',
        "['2020-08-31 12:17 PM']",
        "'2019-06-18 01:41PM",
        '12/9/2019',
        '2020-04-11',
    ]
    expected_list = [
        '',
        '2020-08-31',
        '2019-06-18',
        '2019-12-09',
        '2020-04-11',
    ]
    assert expected_list == [format_date(date) for date in test_list]
