"""
Purpose: To transform and insert Categorically inelligible datasets.

Author : Albert Ulysses <albertulysseschavez@gmail.com>
"""
from operator import itemgetter

import pandas as pd

from database.database import SessionLocal
from database.models import CategoricallyIneligible
from transformations.insert_address import get_address_id
from transformations.normalize_address import normalize_address_wrapper


def normalize_categorically_inelligible(filepath) -> pd.DataFrame:
    """
    Reads in the dataset and returns normalized dataframe.

    :param file: An excel file of Categorically Ineligible data.
    """
    ci_dataframe = pd.read_excel(
        filepath,
        sheet_name='Categorically ineligible',
    )
    ci_dataframe['ADDRESS'] = [
        itemgetter('address_line_1')
        (normalize_address_wrapper(address))
        for address in ci_dataframe['ADDRESS'].tolist()
    ]
    ci_dataframe.rename(
        columns={
            'ADDRESS': 'Address1',
            'UNIT\nNUMBER': 'Address2',
        },
        inplace=True,
    )
    ci_dataframe['City'] = '' 
    # assumes all entries are in California
    ci_dataframe['State'] = 'CA'
    ci_dataframe['Zipcode'] = 0
    ci_dataframe['Prohibited'] = 0
    ci_dataframe.fillna('', inplace=True)
    ci_dataframe.drop_duplicates(inplace=True)
    return ci_dataframe


def normalize_prohibited(filepath) -> pd.DataFrame:
    """
    Reads in the dataset and returns normalized dataframe.

    :param file: An excel file of Prohibited  data.
    """
    prohibited_dataframe = pd.read_excel(
        filepath,
        sheet_name='Prohibited',
    )
    prohibited_dataframe[
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
        )(normalize_address_wrapper(address[:-5]))
        for address in prohibited_dataframe['Address'].tolist()
    ]
    prohibited_dataframe['Prohibited'] = 1
    prohibited_dataframe[
        [
            'ENTIRE BUILDING',
            'MIXED INCOME',
            'ELLIS ACT',
            'LANDLORD REQ BLACKLIST',
            'INCOME RESTRICTED',
            'RSO',
        ]
    ] = 0
    prohibited_dataframe.fillna('', inplace=True)
    prohibited_dataframe['Zipcode'] = [
        0 if type(zip_) != int else zip_
        for zip_ in prohibited_dataframe['Zipcode'].tolist()
    ]
    prohibited_dataframe.drop_duplicates(inplace=True)
    print(prohibited_dataframe.head())
    return prohibited_dataframe


def process_categorically_inelligible(filepath, session):
    """
    Transforms and inserts Categorically Ineligible data into the database.

    :param filepath: An excel file of Categorically Ineligible data.
    :param session: A SQLAlchemy session object.
    """
    ci_dataframe = normalize_categorically_inelligible(filepath)
    prohibited_dataframe = normalize_prohibited(filepath)

    print('start')
    for _, row in pd.concat(
       [ci_dataframe, prohibited_dataframe],
       ignore_index=True,
    ).iterrows():
        address_id = get_address_id(session, row)

        ci_entry = CategoricallyIneligible(
            address_id=address_id,
            entire_building=row['ENTIRE BUILDING'],
            mixed_income=row['MIXED INCOME'],
            ellis_act=row['ELLIS ACT'],
            income_restrict=row['INCOME RESTRICTED'],
            req_blacklist=row['LANDLORD REQ BLACKLIST'],
            rso=row['RSO'],
            prohibited=row['Prohibited'],
        )
        session.add(ci_entry)
        session.commit()
        print('commited CategoricallyIneligible entry')
    print('Finished')


if __name__ == '__main__':
    process_categorically_inelligible(
        '',
        session=SessionLocal(),
    )
