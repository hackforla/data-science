"""
Purpose: To transform and insert tot datasets.

Author : Albert Ulysses <albertulysseschavez@gmail.com>
"""
from operator import itemgetter

import pandas as pd

from database.database import SessionLocal
from database.models import Tot
from transformations.format_date import format_date
from transformations.insert_address import get_address_id
from transformations.normalize_address import normalize_address_wrapper


def normalize_tot(filepath) -> pd.DataFrame:
    """
    Reads in the dataset and returns normalized dataframe.

    :param file: An excel file of tot data.
    """
    tot_dataframe = pd.read_excel(
        filepath,
        sheet_name='TOT payer',
    )
    tot_dataframe[['Address1', 'Address2']] = [
        itemgetter('address_line_1', 'address_line_2')
        (normalize_address_wrapper(address))
        for address in tot_dataframe['STREET_ADDRESS'].tolist()
    ]
    tot_dataframe['Address2'] = [
        ''
        if address is None else address
        for address in tot_dataframe['Address2'].tolist()
    ]
    tot_dataframe['LOCATION_START_DATE'] = [
        format_date(date)
        for date in tot_dataframe['LOCATION_START_DATE'].tolist()
    ]

    tot_dataframe['CERT_EFFECTIVE_DATE'] = [
        format_date(date)
        for date in tot_dataframe['LOCATION_START_DATE'].tolist()
    ]
    tot_dataframe_clean = tot_dataframe[
        [
            'Address1',
            'Address2',
            'CITY',
            'STATE',
            'ZIP_CD',
            'LEGAL_NAME',
            'DBA_NAME',
            'CERT_DESCR',
            'LOCATION_START_DATE',
            'CERT_EFFECTIVE_DATE',
        ]
    ]
    tot_dataframe_clean.rename(
        columns={
            'CITY': 'City',
            'STATE': 'State',
            'ZIP_CD': 'Zipcode',
        },
        inplace=True,
    )
    tot_dataframe_clean.drop_duplicates(inplace=True)
    return tot_dataframe_clean


def process_tot(filepath, session):
    """
    Transforms and inserts TOT data into the database.

    :param filepath: An excel file of tot data.
    :param session: A SQLAlchemy session object.
    """
    tot_dataframe_clean = normalize_tot(filepath)

    for _, row in tot_dataframe_clean.iterrows():
        print('start')
        address_id = get_address_id(session, row)

        tot_entry = Tot(
            address_id=address_id,
            legal_name=row['LEGAL_NAME'],
            dba_name=row['DBA_NAME'],
            cert_description=row['CERT_DESCR'],
            location_start_date=row['LOCATION_START_DATE'],
            cer_effective_date=row['CERT_EFFECTIVE_DATE'],
        )
        session.add(tot_entry)
        session.commit()
        print('commited tot entry')
    print('Finished')


if __name__ == '__main__':
    process_tot(
        '',
        session=SessionLocal(),
    )
