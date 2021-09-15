"""
Purpose: To transform and insert Warning datasets.

Author : Albert Ulysses <albertulysseschavez@gmail.com>
"""
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
) -> pd.DataFrame:
    """
    Reads in the dataset and returns a normalized dataframe.
    This function is for dataset that only have a date and address.

    :param filepath: An excel file with a citations sheet.
    :param sheetname: The excel sheet name.
    """
    dtype={'Date of Citation Notice': 'string'}
    date_address_dataframe = pd.read_excel(filepath, sheet_name=sheetname, dtype=dtype)
    date_address_dataframe['Date of Citation Notice'] = [
        format_date(date) for date in
        date_address_dataframe['Date of Citation Notice'].tolist()
    ]
    # removes odd endings in addresses
    date_address_dataframe['Property Address'] = [
        address[:-9] if address.strip()[-7:] == 'USA, CA' else address.strip()
        for address in date_address_dataframe['Property Address'].tolist()
    ]
    date_address_dataframe['Property Address'] = [
        address[:-14] if address.strip()[-12:] == 'USA, CA , US' else address.strip()
        for address in date_address_dataframe['Property Address'].tolist()
    ]
    date_address_dataframe[
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
            )(normalize_address_wrapper(address[:]))
        for address in date_address_dataframe['Property Address'].tolist()
    ]
    date_address_dataframe[
        [
            'mAddress1',
            'mAddress2',
            'mCity',
            'mState',
            'mZipcode',
            'recipient_name',
            'letter_number',
            'parcel_number',
        ]
    ] = ''
    date_address_dataframe['letter_type'] = 'Citation'
    date_address_dataframe.rename(
        columns={
            'Registration Number': 'registration_number',
            'Date of Citation Notice': 'Date of Letter',
            'Status (5/21)': 'status',
            'Violation Description': 'violation',
            'Fine': 'fine',
        },
        inplace=True,
    )
    date_address_dataframe.fillna('', inplace=True)
    date_address_dataframe['Zipcode'] = [
        0 if zip_.isdigit() == False else int(zip_)
        for zip_ in date_address_dataframe['Zipcode'].tolist()
    ]
    date_address_dataframe['mZipcode'] = [
        0 if zip_.isdigit() == False else int(zip_)
        for zip_ in date_address_dataframe['mZipcode'].tolist()
    ]
    date_address_dataframe['State'] = 'CA'
    date_address_dataframe.drop_duplicates(inplace=True)
    return date_address_dataframe


def process_warnings(
    filepath: str,
    sheetname: str,
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
        sheetname='Citations',
        normalize_function=normalize_date_address_sheet,
        session=SessionLocal(),
    )
