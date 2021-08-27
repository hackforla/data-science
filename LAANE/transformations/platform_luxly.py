"""
Purpose: To transform and insert luxly datasets.

Author : Albert Ulysses <albertulysseschavez@gmail.com>
"""
from operator import itemgetter

import numpy as np
import pandas as pd

from database.database import SessionLocal
from database.models import Platform
from transformations.insert_address import get_address_id
from transformations.normalize_address import normalize_address_wrapper


def normalize_luxly(filepath: str, filetype: str = 'excel') -> pd.DataFrame:
    """
    Reads in the dataset and returns normalized dataframe.

    :param file: A file of luxly data.
    """
    usecols = [
        'Unique Permanent Primary Listing ID',
        'Listing URL',
        'Registration # / Pending Registration Status # / Exemption Status Code',
        'House #',
        'Apt / Suite / Unit #',
        'Unique Host ID',
        'Host Email Address',
        "Listing's Street Address",
    ]
    if filetype == 'csv':
        luxly_dataframe = pd.read_csv(
            filepath,
            usecols=usecols,
            dtype={'House #': 'string', 'Apt / Suite / Unit #': 'string'},
        )
    else:
        luxly_dataframe = pd.read_excel(
            filepath,
            usecols=usecols,
            dtype={'House #': 'string', 'Apt / Suite / Unit #': 'string'},
        )

    luxly_dataframe[
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
        for address in luxly_dataframe["Listing's Street Address"].tolist()
    ]
    luxly_dataframe['Address1'] = np.where(
        luxly_dataframe['House #'].fillna('') == '-',
        luxly_dataframe['Address1'].fillna(''),
        luxly_dataframe['House #'].fillna(''),
    )
    luxly_dataframe['Address2'] = np.where(
        luxly_dataframe['Apt / Suite / Unit #'].fillna('') == '-',
        luxly_dataframe['Address2'].fillna(''),
        luxly_dataframe['Apt / Suite / Unit #'].fillna(''),
    )
    return luxly_dataframe[
        [
            'Address1',
            'Address2',
            'City',
            'State',
            'Zipcode',
            'Unique Permanent Primary Listing ID',
            'Listing URL',
            'Unique Host ID',
            'Host Email Address',
            'Registration # / Pending Registration Status # / Exemption Status Code',
        ]
    ]


def process_luxly(filepath: str, session, filetype: str = 'excel'):
    """
    Transforms and inserts Categorically Ineligible data into the database.

    :param filepath: An excel file of Categorically Ineligible data.
    :param session: A SQLAlchemy session object.
    """
    luxly_clean = normalize_luxly(filepath, filetype)

    print('start')
    for _, row in luxly_clean.iterrows():
        address_id = get_address_id(session, row)

        luxly_entry = Platform(
            address_id=address_id,
            listing_id=row['Unique Permanent Primary Listing ID'],
            listing_url=row['Listing URL'],
            host_id=row['Unique Host ID'],
            host_email=row['Host Email Address'],
            registrant_number=row['Registration # / Pending Registration Status # / Exemption Status Code'],
        )
        session.add(luxly_entry)
        session.commit()
        print('commited tot entry')
    print('Finished')


if __name__ == '__main__':
    process_luxly(
        filepath='',
        filetype='csv',
        session=SessionLocal(),
    )
