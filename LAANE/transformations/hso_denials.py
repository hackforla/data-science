"""
Purpose: To transform and insert HSO_denails datasets.

Author : Albert Ulysses <albertulysseschavez@gmail.com>
"""
from operator import itemgetter
import pandas as pd
from database.database import SessionLocal
from database.models import Address, HSODenials
from transformations.format_date import format_date
from transformations.normalize_address import normalize_address_wrapper


def format_property_unit(property_unit_numner: str) -> str:
    """
    Normalize the property unit number.

    :param property_unit_numner: a property unit value.
    """
    # TODO: refactor this to make it nicer and we make compatible.
    return (
        '{0}/{1}'.format(property_unit_numner[6], property_unit_numner[9])
        if property_unit_numner[-8:] == '00:00:00'
        else
        ''
        if property_unit_numner == '<NA>'
        or
        len(property_unit_numner) > 9
        else
        property_unit_numner.strip()
    )


def process_hso_denials(filepath):
    """Transforms and Inserts HSO denial data into database."""
    # transform and create clean dataframe.
    hso_denial_dataframe = pd.read_excel(filepath, sheet_name='Denials', dtype={'Property Unit Number': "string"})
    hso_denial_dataframe['Address2'] = [format_property_unit(str(property_unit)) for property_unit in hso_denial_dataframe['Property Unit Number'].tolist()]
    hso_denial_dataframe['Application Date'] = [format_date(str(date)) for date in hso_denial_dataframe['Application Date'].tolist()]
    hso_denial_dataframe['Denial Date'] = [format_date(str(date)) for date in hso_denial_dataframe['Denial Date'].tolist()]
    hso_denial_dataframe['Registrant Name'] = [str(name).strip() for name in hso_denial_dataframe['Registrant Name'].tolist()]
    hso_denial_dataframe[['Address1', 'City', 'State', 'Zipcode']] = [itemgetter('address_line_1', 'city', 'state', 'postal_code')(normalize_address_wrapper(address)) for address in hso_denial_dataframe['Property Address'].tolist()]
    hso_denials_clean = hso_denial_dataframe[['Registration Number','Registrant Name', 'Address1', 'Address2', 'City', 'State','Zipcode', 'Application Date', 'Denial Date']]
    hso_denials_clean.drop_duplicates(inplace=True)

    # create session.
    session = SessionLocal()

    # begin to iterateover rows
    for _, row in hso_denials_clean.iterrows():
        # Check for address or enter.
        # TODO: write a function to hide abstraction in the future.
        print('start')
        address = (
            session.query(Address).filter(
                Address.address1 == row['Address1'],
                Address.address2 == row['Address2'],
                Address.city == row['City'],
                Address.state == row['State'],
                Address.zipcode == row['Zipcode'],
            ).one_or_none()
        )
        if address is None:
            address = Address(
                address1 = row['Address1'],
                address2 = row['Address2'],
                city = row['City'],
                state = row['State'],
                zipcode = row['Zipcode'],
            )
            session.add(address)
            session.commit()
            print('commited address')

        # enter hso_denials
        hso_denials_entry = HSODenials(
            address_id = address.address_id,
            registrant_name = row['Registrant Name'],
            application_date = row['Application Date'],
            denial_date = row['Denial Date'],
        )
        session.add(hso_denials_entry)
        session.commit()
        print('commited hso denial')
        print('successful')


if __name__ == '__main__':
    pass
