"""
Purpose: To transform and insert exempt datasets.

Author : Albert Ulysses <albertulysseschavez@gmail.com>
"""
from operator import itemgetter

import pandas as pd

from database.database import SessionLocal
from database.models import Exempt
from transformations.insert_address import get_address_id
from transformations.normalize_address import normalize_address_wrapper


def normalize_tors_bnb(filepath: str) -> pd.DataFrame:
    """
    Reads in the tors and bnb datasets and returns normalized dataframe.

    :param file: An excel file with an exempt sheet.
    """
    tors_dataframe = pd.read_excel(
        filepath,
        sheet_name='TORS',
    )
    bnb_dataframe = pd.read_excel(filepath, sheet_name='B&B')

    tors_dataframe['exempt_type'] = 'TORS'
    bnb_dataframe['exempt_type'] = 'B&B'
    tors_bnb_dataframe = pd.concat(
        [tors_dataframe, bnb_dataframe],
        ignore_index=True,
    )

    tors_bnb_dataframe[
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
        for address in tors_bnb_dataframe['Address'].tolist()
    ]
    tors_bnb_dataframe['State'] = 'CA'
    tors_bnb_dataframe[
        [
            'host_apn',
            'subtype',
        ]
    ] = ''
    tors_bnb_dataframe.fillna('', inplace=True)
    tors_bnb_dataframe['Zipcode'] = [
        0 if zip_.isdigit() == False else int(zip_)
        for zip_ in tors_bnb_dataframe['Zipcode'].tolist()
    ]
    tors_bnb_dataframe.drop(['Address', 'Permit ID1'], axis=1, inplace=True)
    tors_bnb_dataframe.drop_duplicates(inplace=True)
    return tors_bnb_dataframe


def normalize_hotels(filepath: str) -> pd.DataFrame:
    """
    Reads in the tors and bnb datasets and returns normalized dataframe.

    :param file: An excel file with an exempt sheet.
    """
    hotels_dataframe = pd.read_excel(
        filepath,
        sheet_name='hotels',
        dtype={'ZIP_CD': 'string'},
    )

    hotels_dataframe[
        [
            'Address1',
            'Address2',
        ]
    ] = [
        itemgetter(
            'address_line_1',
            'address_line_2',
        )(normalize_address_wrapper(address))
        for address in hotels_dataframe['ADDRESS'].tolist()
    ]
    hotels_dataframe.drop(['ADDRESS'], axis=1, inplace=True)
    hotels_dataframe.rename(
        columns={
            'TYPE': 'subtype',
            'ZIP_CD': 'Zipcode',
            'HOST_APN': 'host_apn',
        },
        inplace=True,
    )
    hotels_dataframe['exempt_type'] = 'hotels'
    hotels_dataframe['State'] = 'CA'
    hotels_dataframe['City'] = ''
    hotels_dataframe.fillna('', inplace=True)
    hotels_dataframe['Zipcode'] = [
        0 if zip_.isdigit() == False else int(zip_)
        for zip_ in hotels_dataframe['Zipcode'].tolist()
    ]
    hotels_dataframe.drop_duplicates(inplace=True)
    return hotels_dataframe


def process_exempt(filepath: str, session):
    """
    Transforms and inserts Categorically Ineligible data into the database.

    :param filepath: An excel file of Categorically Ineligible data.
    :param session: A SQLAlchemy session object.
    """
    tors_bnb_dataframe = normalize_tors_bnb(filepath)
    hotels_dataframe = normalize_hotels(filepath)

    print('start')
    for _, row in pd.concat(
        [tors_bnb_dataframe, hotels_dataframe],
        ignore_index=True,
    ).iterrows():
        address_id = get_address_id(session, row)

        exempt_entry = Exempt(
            address_id=address_id,
            host_apn=row['host_apn'],
            exempt_type=row['exempt_type'],
            subtype=row['subtype'],
        )
        session.add(exempt_entry)
        session.commit()
        print('commited exempt entry')
    print('Finished')


if __name__ == '__main__':
    process_exempt(
        '',
        session=SessionLocal(),
    )
