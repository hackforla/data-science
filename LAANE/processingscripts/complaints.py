"""
Purpose: To transform and insert Complaints datasets.

Author : Albert Ulysses <albertulysseschavez@gmail.com>
"""
from operator import itemgetter

import pandas as pd

from database.database import SessionLocal
from database.models import Complaints
from transformations.format_date import format_date
from transformations.insert_address import get_address_id
from transformations.normalize_address import normalize_address_wrapper


def normalize_complaints(filepath) -> pd.DataFrame:
    """
    Reads in the dataset and resutrns a normalized dataframe.

    :param filepath: An excel file with a Complaints sheet.
    """
    complaints_dataframe = pd.read_excel(
        filepath,
        dtype={'Call Time': 'string'},
    )
    complaints_dataframe['Call Time'] = [
        format_date(call_time)
        for call_time in complaints_dataframe['Call Time'].tolist()
    ]
    complaints_dataframe[
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
        for address in complaints_dataframe['Reported Address'].tolist()
    ]
    complaints_clean = complaints_dataframe[
        [
            'Call Time',
            'Caller Name',
            'Address1',
            'Address2',
            'City',
            'State',
            'Zipcode',
            'Reported Issue',
            'Complaint Type',
            'Unit Permit/Registration Number',
        ]
    ]
    complaints_clean.fillna('', inplace=True)
    complaints_clean['Zipcode'] = [
        0 if type(zip_) != int else int(zip_)
        for zip_ in complaints_clean['Zipcode'].tolist()
    ]
    complaints_clean['State'] = [
        '' if len(state) > 2 else state
        for state in complaints_clean['State'].tolist()
    ]
    complaints_clean.drop_duplicates(inplace=True)
    return complaints_clean


def process_complaints(filepath, session):
    """
    Transforms and inserts Complaints data into the database.

    :param filepath: An excel file of complaints data.
    :param session: A SQLAlchemy session object.
    """
    complaints_clean = normalize_complaints(filepath)

    print('start')
    for _, row in complaints_clean.iterrows():
        address_id = get_address_id(session, row)

        complaint_entry = Complaints(
            address_id=address_id,
            registration_number=row['Unit Permit/Registration Number'],
            complaint_type=row['Complaint Type'],
            call_time=row['Call Time'],
            caller_name=row['Caller Name'],
            reported_issue=row['Reported Issue'],
        )
        session.add(complaint_entry)
        session.commit()
        print('committed complaint entry')
    print('Finished')


if __name__ == '__main__':
    process_complaints(
        '',
        session=SessionLocal(),
    )
