"""
Purpose: To transform and insert Warning datasets.

Author : Albert Ulysses <albertulysseschavez@gmail.com>
"""
# this file only inserts warnings that have a date and address
from operator import itemgetter

import pandas as pd

from database.database import SessionLocal
from database.models import Citation, RecipientMailing, Warnings
from transformations.format_date import format_date
from transformations.insert_address import get_address_id
from transformations.normalize_address import normalize_address_wrapper

def normalize_date_address_sheet(
    filepath: str,
    sheetname: str,
    warningtype: str,
) -> pd.DataFrame:
    """
    Reads in the dataset and returns a normalized dataframe.
    This function is for dataset that only have a date and address.

    :param filepath: An excel file with a Complaints sheet.
    :param sheetname: The excel sheet name.
    """
    dtype={'Date of Letter': 'string'}
    date_address_dataframe = pd.read_excel(filepath, sheet_name=sheetname, dtype=dtype)
    date_address_dataframe['Date of Letter'] = [
        format_date(date) for date in
        date_address_dataframe['Date of Letter'].tolist()
    ]
    date_address_dataframe[
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
        for address in date_address_dataframe['Property Address'].tolist()
    ]
    date_address_dataframe[
        [
            'parcel_number',
            'letter_number',
            'recipient_name',
            'mAddress1',
            'mAddress2',
            'mCity',
            'mState',
            'mZipcode',
            'registration_number',
            'fine',
            'status',
            'violation',
        ]
    ] = ''
    date_address_dataframe['letter_type'] = warningtype 
    date_address_dataframe.fillna('', inplace=True)
    date_address_dataframe['Zipcode'] = [
        0 if type(zip_) != int else zip_
        for zip_ in date_address_dataframe['Zipcode'].tolist()
    ]
    date_address_dataframe['State'] = 'CA'
    date_address_dataframe.drop_duplicates(inplace=True)
    return date_address_dataframe


def process_warnings(
    filepath: str,
    sheetname: str,
    warningtype: str,
    normalize_function,
    session,
):
    """
    Transforms and inserts Warning data into the database.

    :param filepath: An excel file of complaints data.
    :param sheetname: the name of the sheet that is being processed.
    :param normalize_function: the function for normalizing the sheet.
    :param session: A SQLAlchemy session object.
    """
    warning_dataframe = normalize_function(
        filepath,
        sheetname,
        warningtype,
        )
    print('start')
    for _, row in warning_dataframe.iterrows():
        address_id = get_address_id(session, row)

        maddress = (
            session.query(RecipientMailing).filter(
                RecipientMailing.address1 == row['mAddress1'],
                RecipientMailing.address2 == row['mAddress2'],
                RecipientMailing.city == row['mCity'],
                RecipientMailing.state == row['mState'],
                RecipientMailing.zipcode == row['mZipcode'],
            ).one_or_none()
        )
        if maddress is None:
            maddress = RecipientMailing(
                address1=row['mAddress1'],
                address2=row['mAddress2'],
                city=row['mCity'],
                state=row['mState'],
                zipcode=row['mZipcode'],
            )
            session.add(maddress)
            session.commit()

        warning_entry = Warnings(
            address_id=address_id,
            recipient_mailing_id=maddress.recipient_mailing_id,
            parcel_number=row['parcel_number'],
            letter_number=row['letter_number'],
            letter_type=row['letter_type'],
            recipient_name=row['recipient_name'],
            date_of_letter=row['Date of Letter'],
        )
        session.add(warning_entry)
        session.commit()

        citation_entry = Citation(
            warning_id=warning_entry.warning_id,
            registration_number=row['registration_number'],
            fine=row['fine'],
            status=row['status'],
            violation=row['violation'],
        )
        session.add(citation_entry)
        session.commit()
        print('entered citation, warning and maddress')
    print('finished')



if __name__ == '__main__':
    process_warnings(
        filepath='',
        sheetname='',
        warningtype='',
        normalize_function=normalize_date_address_sheet,
        session=SessionLocal(),
    )
