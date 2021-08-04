#!/usr/bin/env python3
"""tests for assessor_table."""
import numpy as np
import pandas as pd
from pandas.testing import assert_series_equal

from transformations.assessor_table import (
    address1,
    city,
    owner_names,
    special_name_assessee,
    trust_name,
)

# TODO: refactor to match WEWORK Style guide
def test_owner_names():
    """Tests the function owner_names."""
    expected_owner_names = [
        'PATEL HANISH B ALPA P',
        "ALI HOSSAN",
        "ABANILLA ALBERTO R SYLVANA R ABANILLA LIANNE M",
        "POPAL ARINA POPAL MALIHA",
    ]
    ser = pd.Series(expected_owner_names, name="Owner Names")

    first_owner_name = [
        "PATEL,HANISH B AND ALPA P TRS",
        "ALI,HOSSAN",
        "ABANILLA,ALBERTO R AND",
        "POPAL,ARINA AND",
    ]

    df = pd.DataFrame(
        {
            "First Owner Name": first_owner_name,
            "First Owner Name Overflow": ["PATEL TRUST", "", "SYLVANA R AND", ""],
            "Second Owner Name": ["", "", "ABANILLA,LIANNE M", "POPAL,MALIHA"],
        }
    )
    assert_series_equal(owner_names(df), ser)


def test_trust_name():
    items = ["PATEL TRUST", "", ""]
    ser = pd.Series(items, name="Trust Name")
    first_owner_over = ["PATEL TRUST", "", "SYLVANA R AND"]
    df = pd.DataFrame({"First Owner Name Overflow": first_owner_over})
    assert_series_equal(trust_name(df), ser)


def test_special_name_assessee():
    items = [
            "JOHN SCULL",
            "REAL ESTATE BUS GROUP-JUNE",
            "TRANSPLANT DIAGNOSTICS (TDX)",
            ""
    ]
    ser = pd.Series(items, name="Special Name Assessee Clean")
    special_names = [
            "C/O JOHN SCULL ",
            "REAL ESTATE BUS GROUP-JUNE",
            "C/O TRANSPLANT DIAGNOSTICS (TDX)",
            ""
    ]
    df = pd.DataFrame({"Special Name Assessee": special_names})
    assert_series_equal(special_name_assessee(df), ser)


def test_address1():
    # row 2894
    items = [
            "8311 N PEYTON WAY",
            np.nan,
            "23135 SCHOENBORN STREET",
            "23916 1/2 LOS ROSAS STREET",
            "23931 JENSEN DRIVE"
    ]
    ser = pd.Series(items, name="Address1")
    house_no = [
            8311,
            0,
            23135,
            23916,
            23931
    ]
    fraction = [
            "",
            np.nan,
            "$  ",
            "2021-01-02 00:00:00",
            ""
    ]
    direction = [
            "N",
            "",
            "",
            "",
            ""
    ]
    street_name = [
            "PEYTON WAY",
            np.nan,
            "SCHOENBORN ST",
            "LOS ROSAS ST",
            "JENSEN DR    "

    ]
    df = pd.DataFrame({
        "Situs House No": house_no,
        "Fraction": fraction,
        "Direction": direction,
        "Street Name": street_name
        })

    assert_series_equal(address1(df, "Situs House No", "Fraction", "Direction", "Street Name"), ser)


def test_city():
    items = ["LOS ANGELES", "CANOGA PARK", np.nan, 'PALM BEACH GARDENS']
    ser = pd.Series(items, name="City")
    city_state = ["LOS ANGELES CA          ", "CANOGA PARK             ", "                        ", 'PALM BEACH GARDENS FL   ']
    df = pd.DataFrame({"City State": city_state})

    assert_series_equal(city(df["City State"]), ser)
