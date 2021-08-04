#!/usr/bin/env python3
"""
Purpose: Transform assesor data to make Assessor table compatible.

Author : Albert Ulysses <albertulysseschavez@gmail.com>
"""

import numpy as np
import pandas as pd

# TODO: refactor to match WEMAKE STYLEGUIDE


def owner_names(assessor_dataframe: pd.DataFrame) -> pd.Series:
    """
    Transformations for the Owner Names column from a raw assesor dataframe.

    :param dataframe: a raw assessor dataframe.
    """
    first_owner_name_overflow = 'First Owner Name Overflow'

    assessor_dataframe['First Owner Name Clean'] = (
        assessor_dataframe['First Owner Name']
        .str.strip()
        .str.replace(',', ' ')
        .str.replace(' AND ', ' ')
        .str.replace(' AND', ' ')
        .str.replace(' TRS', '')
        .str.replace(' TR', '')
    )
    assessor_dataframe['First Owner Name Continued'] = np.where(
        assessor_dataframe[first_owner_name_overflow].str.contains(' TRUST') == False,
        assessor_dataframe[first_owner_name_overflow]
        .str.strip()
        .str.replace(',', ' ')
        .str.replace(' AND ', ' ')
        .str.replace(' AND', ' ')
        .str.replace(' TRS', '')
        .str.replace(' TR', ''),
        '',
    )
    assessor_dataframe['Second Owner Name Clean'] = (
        assessor_dataframe['Second Owner Name'].str.strip().str.replace(',', ' ')
    )
    assessor_dataframe['Owner Names'] = (
        assessor_dataframe['First Owner Name Clean']
        .str.cat(assessor_dataframe['First Owner Name Continued'], sep=' ', na_rep='')
        .str.cat(assessor_dataframe['Second Owner Name Clean'], sep=' ', na_rep='')
        .str.replace(r'\s+', ' ', regex=True)
        .str.strip()
    )

    return assessor_dataframe['Owner Names']


def trust_name(assessor_dataframe: pd.DataFrame) -> pd.Series:
    """
    Transformation for the trust column.

    :param assessor_dataframe: a raw assessor_dataframe.
    """

    assessor_dataframe["Trust Name"] = np.where(
        assessor_dataframe["First Owner Name Overflow"].str.contains(" TRUST") == True,
        assessor_dataframe["First Owner Name Overflow"],
        "",
    )
    return assessor_dataframe["Trust Name"]


def special_name_assessee(df: pd.DataFrame) -> pd.Series:
    """Special name assessee clean"""
    df["Special Name Assessee Clean"] = (
        df["Special Name Assessee"]
        .str.replace("DBA", "")
        .str.replace("C/O", "")
        .str.replace("TR #", "")
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )
    return df["Special Name Assessee Clean"]


def address1(
    df: pd.DataFrame, house_no: str, fraction: str, direction: str, street_name: str
) -> pd.Series:
    """address1"""
    # Ending of streets Dictionary
    end_dict = {
        "AVE": "AVENUE",
        "BLVD": "BOULEVARD",
        "CIR": "CIRCLE",
        "CT": "COURT",
        "DR": "DRIVE",
        "LN": "LANE",
        "PL": "PLACE",
        "ST": "STREET",
        "RD": "ROAD",
        "TERR": "TERRACE",
        "TER": "TERRACE",
        "TRL": "TRAIL",
        "WY": "WAY",
    }

    # street transformation
    df[["Street Name Clean", "Ending"]] = (
        df[street_name].str.strip().str.rsplit(" ", 1, expand=True)
    )

    df["Ending Clean"] = df["Ending"].replace(end_dict)

    # will have to work on this when dealing with the large datasets

    df["Fraction Clean"] = (
        (df[fraction].astype(str).str[6] + "/" + df[fraction].astype(str).str[9])
        if len(df[fraction].astype(str).str[:]) > 3
        else (df[fraction].astype(str))
    )

    df["Address1"] = np.where(
        df[house_no].astype(str).str.strip() == "0",
        np.nan,
        df[house_no]
        .astype(str)
        .str.cat(df["Fraction Clean"].str.strip(), sep=" ", na_rep="")
        .str.cat(df[direction].str.strip(), sep=" ", na_rep="")
        .str.cat(df["Street Name Clean"], sep=" ", na_rep="")
        .str.cat(df["Ending Clean"], sep=" ", na_rep="")
        .str.replace(r"\s+", " ", regex=True),
    )
    return df["Address1"]


def city(ser: pd.Series) -> pd.Series:
    # city
    # Current list of all US states abbriviated.
    two_letter_states = [
        "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
        "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
        "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
        "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
        "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
    ]
    cities = np.where(
        ser.str.strip().str[-2:].str.contains("|".join(two_letter_states)) == False,
        ser.str.strip().replace('', np.nan),
        ser.str.strip().str[:-2].str.strip(),
    )
    return pd.Series(cities, name="City")


def main():
    """
    TODO: REFACTOR into seperate file.
    """
    df = pd.read_excel("/home/albertulysses/Downloads/DS04 - Part 3.xlsx")

    # owner names
    df['Owner Names'] = owner_names(df)

    # Trust Name
    df['Trust Name'] = trust_name(df)

    # Special Name Assessee
    df['Special Name Assessee Clean'] = special_name_assessee(df)

    # Special Name Assessee legend
    df["Special Name Legend"] = df["Special Name Legend"].str.strip()

    # Address 1
    df['Address1'] = address1(df, 'Situs House No', 'Fraction', 'Direction', 'Street Name')

    # Address 2
    df["Address2"] = df["Unit"].str.strip().str.replace(r"\s+", " ", regex=True)

    # city
    df['City'] = city(df['City State'])

    # State
    df["State"] = "CA"

    # zip
    df["Zipcode"] = df["Zip"].astype(str).str[:5].astype(int)

    # declare new dataframe
    assesor_df = df[
        [
            "Owner Names",
            "Trust Name",
            "AIN",
            "Agency Number",
            "Special Name Assessee",
            "Special Name Legend",
            "Homeowner Exemption Val",
            "Landlord Reappraisal Year",
            "Landlord Units",
            "Address1",
            "Address2",
            "City",
            "State",
            "Zipcode",
        ]
    ]

    # process files into 10 files

    for idx, chunk in enumerate(np.array_split(assesor_df, 10)):
        chunk.to_csv("CSVprocessed/DSO43_{0}.csv".format(idx))


if __name__ == "__main__":
    main()
