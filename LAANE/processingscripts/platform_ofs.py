"""
Purpose: To transform and insert one fine stay (ofs) datasets.

Author : Albert Ulysses <albertulysseschavez@gmail.com>
"""
from operator import itemgetter
import os
import glob

import numpy as np
import pandas as pd

from database.database import SessionLocal
from database.models import Platform
from transformations.insert_address import get_address_id
from transformations.normalize_address import normalize_address_wrapper


def normalize_ofs(filepath: str) -> pd.DataFrame:
    """
    Reads in the dataset and returns normalized dataframe.

    :param file: A file of ofs data.
    """
    usecols = [
        'house_number',
        'unit_number',
        'situs_address',
        'listing_id',
        'listing_urls',
        'unique_host_id',
        'host_email_address',
        'registration_number',
    ]

    dtypes = {
        'house_number': 'string',
        'unit_number': 'string',
    }
    ofs_dataframe = pd.read_csv(filepath, usecols=usecols, dtype=dtypes)
    ofs_dataframe[
        [
            'Address1',
            'Address2',
            'City',
            'Zipcode',
        ]
    ] = [
        itemgetter(
            'address_line_1',
            'address_line_2',
            'city',
            'postal_code',
        )(normalize_address_wrapper(address))
        for address in ofs_dataframe['situs_address'].tolist()
    ]
    ofs_dataframe['State'] = 'CA'
    ofs_dataframe['Address1'] = np.where(
        ofs_dataframe['Address1'].fillna('') == '',
        str(ofs_dataframe['house_number']),
        np.nan,
    )
    ofs_dataframe['Address2'] = np.where(
        ofs_dataframe['Address2'].fillna('') == '',
        str(ofs_dataframe['unit_number']),
        np.nan,
    )
    return ofs_dataframe[
        [
            'Address1',
            'Address2',
            'City',
            'State',
            'Zipcode',
            'listing_id',
            'listing_urls',
            'unique_host_id',
            'host_email_address',
            'registration_number',
        ]
    ]


def process_ofs(filepath: str, session):
    """
    Transforms and inserts Categorically Ineligible data into the database.

    :param filepath: An excel file of Categorically Ineligible data.
    :param session: A SQLAlchemy session object.
    """
    ofs_dataframe = normalize_ofs(filepath)

    print('start')
    for _, row in ofs_dataframe.iterrows():
        address_id = get_address_id(session, row)

        platform_entry = Platform(
            address_id=address_id,
            listing_id=row['listing_id'],
            listing_url=row['listing_urls'],
            host_id=row['unique_host_id'],
            host_email=row['host_email_address'],
            registrant_number=row['registration_number'],
        )
        session.add(platform_entry)
        session.commit()
        print('commited platform entry')
    print('Finished')


if __name__ == '__main__':
    filepath=''
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.csv'))
        for f in files:
            all_files.append(os.path.abspath(f))
    num_files = len(all_files)

    for i, datafile in enumerate(all_files, 1):
        process_ofs(
            datafile,
            session=SessionLocal(),
        )
        print('{}/{} files processed.'.format(i, num_files))
