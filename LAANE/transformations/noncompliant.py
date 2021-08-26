"""
Purpose: To transform and insert noncompliant datasets.

Author : Albert Ulysses <albertulysseschavez@gmail.com>
"""
from operator import itemgetter

import pandas as pd

from database.database import SessionLocal
from database.models import Noncompliant
from transformations.insert_address import get_address_id
from transformations.normalize_address import normalize_address_wrapper


def normalize_noncompliant_32020_sheet(filepath: str) -> pd.DataFrame:
    """
    Normalize the Noncompliant 3-20-20 data.

    :param filepath: A file path of an excel sheet.
    """
    noncompliant_32020_dataframe = pd.read_excel(
        filepath,
        sheet_name='3-20-20',
    )

    noncompliant_32020_dataframe['date_generated'] = '2020-03-20'

    # strip the last 5 if it ends in USA otherwise remove United states ending
    noncompliant_32020_dataframe['address'] = [
        address.strip()[:-5] if address.strip()[:-3] == 'USA'
        else address.strip()[:-15]
        for address in noncompliant_32020_dataframe['address'].tolist()
    ]

    noncompliant_32020_dataframe[
        [
            'Address1',
            'Address2',
            'City',
            'State',
            'Zipcode',
        ]
    ] = [
        itemgetter(
            'address_line_1',
            'address_line_2',
            'city',
            'state',
            'postal_code',
        )(normalize_address_wrapper(address))
        for address in noncompliant_32020_dataframe['address'].tolist()
    ]
    noncompliant_32020_dataframe.rename(
        columns={
            'unit_number': 'Address2',
        },
    )
    noncompliant_32020_dataframe['Address2'] = [
        '' if (unit == None) or (unit == 'Not yet identified') else unit
        for unit in noncompliant_32020_dataframe['Address2'].tolist()
    ]
    noncompliant_32020_dataframe['land_use'] = None
    noncompliant_32020_clean = noncompliant_32020_dataframe[
        [
            'Address1',
            'Address2',
            'City',
            'State',
            'Zipcode',
            'parcel_number',
            'permit_number',
            'case_number',
            'listing_url',
            'listing_title',
            'listing_property_type',
            'listing_room_type',
            'land_use',
            'compliance_explanation',
            'date_generated',
        ]
    ]
    noncompliant_32020_clean.drop_duplicates(inplace=True)
    return noncompliant_32020_clean


def normalize_noncompliant_52121_sheet(filepath: str) -> pd.DataFrame:
    """
    Normalize the Noncompliant 5-21-21 data.

    :param filepath: A file path of an excel sheet.
    """
    noncompliant_52121_dataframe = pd.read_excel(
        filepath,
        sheet_name='5-21-21',
        dtype={'Address': 'string'},
    )

    noncompliant_52121_dataframe['date_generated'] = '2021-05-21'

    # strip the last 5 if it ends in USA otherwise remove United states ending
    noncompliant_52121_dataframe['Address'] = [
        address.strip()[:-5] if address.strip()[:-3] == 'USA'
        else address.strip()[:-15]
        for address in noncompliant_52121_dataframe['Address'].fillna('').tolist()
    ]

    noncompliant_52121_dataframe[
        [
            'Address1',
            'City',
            'State',
            'Zipcode',
        ]
    ] = [
        itemgetter(
            'address_line_1',
            'city',
            'state',
            'postal_code',
        )(normalize_address_wrapper(address))
        for address in noncompliant_52121_dataframe['Address'].tolist()
    ]
    noncompliant_52121_dataframe.rename(
        columns={
            'Unit Number': 'Address2',
            'Land Use Compliance Status': 'land_use',
            'Listing URL': 'listing_url',
            'Parcel Number': 'parcel_number',
        },
        inplace=True,
    )
    noncompliant_52121_dataframe['Address2'] =[
        '' if unit == None else unit
        for unit in noncompliant_52121_dataframe['Address2'].tolist()
    ]
    noncompliant_52121_dataframe[
        [
            'permit_number',
            'case_number',
            'listing_title',
            'listing_property_type',
            'listing_room_type',
            'compliance_explanation',
        ]
    ] = None
    noncompliant_52121_clean = noncompliant_52121_dataframe[
        [
            'Address1',
            'Address2',
            'City',
            'State',
            'Zipcode',
            'parcel_number',
            'permit_number',
            'case_number',
            'listing_url',
            'listing_title',
            'listing_property_type',
            'listing_room_type',
            'land_use',
            'compliance_explanation',
            'date_generated',
        ]
    ]
    noncompliant_52121_clean.drop_duplicates(inplace=True)
    return noncompliant_52121_clean


def process_noncompliant(filepath: str, session):
    """
    Transforms and inserts Categorically Ineligible data into the database.

    :param filepath: An excel file of Categorically Ineligible data.
    :param session: A SQLAlchemy session object.
    """
    noncompliant_32020_clean = normalize_noncompliant_32020_sheet(filepath)
    noncompliant_52121_clean = normalize_noncompliant_52121_sheet(filepath)

    print('start')
    for _, row in pd.concat(
        [noncompliant_32020_clean, noncompliant_52121_clean],
        ignore_index=True,
    ).iterrows():
        address_id = get_address_id(session, row)

        noncompliant_entry = Noncompliant(
            address_id=address_id,
            parcel_number=row['parcel_number'],
            permit_number=row['permit_number'],
            case_number=row['case_number'],
            listing_url=row['listing_url'],
            listing_title=row['listing_title'],
            listing_property_type=row['listing_property_type'],
            listing_room_type=row['listing_room_type'],
            land_use=row['land_use'],
            compliance_explanation=row['compliance_explanation'],
            date_generated=row['date_generated'],
        )
        session.add(noncompliant_entry)
        session.commit()
        print('commited Noncompliant entry')
    print('Finished')


if __name__ == '__main__':
    process_noncompliant(
        '',
        session=SessionLocal(),
    )
