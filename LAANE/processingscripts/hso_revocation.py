"""
Purpose: To transform and insert hso revocation datasets.

Author : Albert Ulysses <albertulysseschavez@gmail.com>
"""
from operator import itemgetter

import pandas as pd

from database.database import SessionLocal
from database.models import HSORevocation
from transformations.format_date import format_date
from transformations.insert_address import get_address_id
from transformations.normalize_address import normalize_address_wrapper


def normalize_hso_revocation(filepath: str) -> pd.DataFrame:
    """
    Reads in the dataset and returns normalized dataframe.

    :param file: An excel file of hso revocation data.
    """
    revocation_dataframe = pd.read_excel(
        filepath,
        sheet_name='Revocations',
        dtype={'Date Revoked': 'string'},
    )

    revocation_dataframe[
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
        for address in revocation_dataframe['Registered Address'].tolist()
    ]

    revocation_dataframe['Date Revoked'] = [
        format_date(date)
        for date in revocation_dataframe['Date Revoked'].tolist()
    ]
    revocation_dataframe.fillna('', inplace=True)
    revocation_dataframe['Address2'] = ''
    revocation_dataframe['Zipcode'] = [
        0 if type(zip_) != int else zip_
        for zip_ in revocation_dataframe['Zipcode'].tolist()
    ]
    revocation_dataframe.drop_duplicates(inplace=True)
    return revocation_dataframe


def process_hso_revocation(filepath: str, session):
    """
    Transforms and inserts hso revoked data into the database.

    :param filepath: An excel file of Categorically Ineligible data.
    :param session: A SQLAlchemy session object.
    """
    revocation_dataframe = normalize_hso_revocation(filepath)

    print('start')
    for _, row in revocation_dataframe.iterrows():
        address_id = get_address_id(session, row)

        hso_revoked_entry = HSORevocation(
            address_id=address_id,
            registration_number=row['Registration Number'],
            registrant_name=row['Permit Holder Name'],
            revoked_date=row['Date Revoked'],
        )
        session.add(hso_revoked_entry)
        session.commit()
        print('commited HSO Revoked entry')
    print('Finished')


if __name__ == '__main__':
    process_hso_revocation(
        '/home/albertulysses/Downloads/LAANE/City of LA data/LA HSO Enforcement - new master 521.xlsx',
        session=SessionLocal(),
    )
