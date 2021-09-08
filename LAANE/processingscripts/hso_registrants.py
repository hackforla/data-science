"""
Purpose: To transform and insert HSO_Registrants datasets.

Author : Albert Ulysses <albertulysseschavez@gmail.com>
"""
from operator import itemgetter

import pandas as pd

from database.database import SessionLocal
from database.models import HSOPlatforms, HSORegistrant
from transformations.insert_address import get_address_id
from transformations.normalize_address import normalize_address_wrapper


def normalize_registrants(
    filepath: str,
    sheetname: str,
    generated_date: str,
) -> pd.DataFrame:
    """
    Reads in the dataset and resutrns a normalized dataframe.

    :param filepath: An excel file with a Complaints sheet.
    :param sheetname: The excel sheet name.
    :param generated_date: The date the sheet was generated.
    """
    usecols = [
        'Registration Number',
        'Property Address',
        'Property Unit Number',
        'Registrant Name',
        'Platforms',
    ]
    registrant_dataframe = pd.read_excel(
        filepath,
        sheet_name=sheetname,
        usecols=usecols,
    )
    registrant_dataframe['Property Address'] = [
        address[:-5] if address[-3:] == 'USA' else address
        for address in registrant_dataframe['Property Address'].tolist()
    ]
    registrant_dataframe[
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
        for address in registrant_dataframe['Property Address'].tolist()
    ]
    registrant_dataframe.rename(
        columns={'Property Unit Number': 'Address2'},
        inplace=True,
    )
    registrant_clean = registrant_dataframe[
        [
            'Address1',
            'Address2',
            'City',
            'State',
            'Zipcode',
            'Registration Number',
            'Registrant Name',
            'Platforms',
        ]
    ]
    registrant_clean['Address2'].fillna('', inplace=True)
    registrant_clean.drop_duplicates(inplace=True)
    registrant_clean['Date Generated'] = generated_date
    return registrant_clean


def process_registrants(filepath, sheetname, generated_date, session):
    """
    Transforms and inserts Complaints data into the database.

    :param filepath: An excel file of complaints data.
    :param sheetname: the name of the sheet that is being processed.
    :param generated_date: The date the file was generated in yyyy-mm-dd.
    :param session: A SQLAlchemy session object.
    """
    registrant_clean = normalize_registrants(
        filepath=filepath,
        sheetname=sheetname,
        generated_date=generated_date,
    )

    print('start')
    for _, row in registrant_clean.iterrows():
        address_id = get_address_id(session, row)

        hso_platform = (
            session.query(HSOPlatforms).filter(
                HSOPlatforms.platforms == row['Platforms'],
            ).one_or_none()
        )
        if hso_platform is None:
            hso_platform = HSOPlatforms(
                platforms=row['Platforms'],
            )
            session.add(hso_platform)
            session.commit()

        hso_registrant_entry = HSORegistrant(
            address_id=address_id,
            hso_platforms_id=hso_platform.hso_platforms_id,
            registration_number=row['Registration Number'],
            registrant_name=row['Registrant Name'],
            generated_date=generated_date,
        )
        session.add(hso_registrant_entry)
        session.commit()
        print('committed hso_registrant entry')


if __name__ == '__main__':
    process_registrants(
        filepath='',
        sheetname='',
        generated_date='',
        session=SessionLocal(),
    )
