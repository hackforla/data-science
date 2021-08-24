"""Tests for HSO denials."""
from transformations.hso_denials import format_property_unit 


def test_format_property_unit():
    """Test the function for format_address2."""
    assert format_property_unit('<NA>') == '' 
    assert format_property_unit('2021-01-02 00:00:00') == '1/2'
    assert format_property_unit('2021-03-04 00:00:00') == '3/4'
    assert format_property_unit('213 ') == '213'
    assert format_property_unit('814 N. Coronado St') == ''
