"""
Purpose: To transform and normalize Assessor data.

Author : Albert Ulysses <albertulysseschavez@gmail.com>
"""
import re
from typing import List
from operator import itemgetter

import pandas as pd

from database.database import SessionLocal
from database.models import Assessor, AssessorMailing
from transformations.insert_address import get_address_id
from transformations.normalize_address import normalize_address_wrapper
from transformations.process_multiple_files import multiple_files


def owner_names(assessor_dataframe: pd.DataFrame) -> List[str]:
    """
    Transformations for the Owner Names column from a raw assesor dataframe.

    :param dataframe: a raw assessor dataframe.
    """
    first_owner_names = [
        first_owner_name.
        strip().replace(',', ' ').
        replace(' AND ', ' ').
        replace(' AND', ' ').
        replace(' TRS', '').
        replace(' TR', '')
        for first_owner_name in
        assessor_dataframe['First Owner Name'].tolist()
    ]

    first_owner_name_continued = [
        first_owner_name_overflow.
        strip().
        replace(',', ' ').
        replace(' AND ', ' ').
        replace(' AND', ' ').
        replace(' TRS', '').
        replace(' TR', '')
        if ' TRUST' not in first_owner_name_overflow
        else ''
        for first_owner_name_overflow in
        assessor_dataframe['First Owner Name Overflow'].tolist()
    ]

    second_owner_names = [
        second_owner_name.
        strip().
        replace(',', ' ')
        for second_owner_name in
        assessor_dataframe['Second Owner Name']
    ]

    return [
        re.sub(r'\s+', ' ', ' '.join(names).strip())
        for names in
        zip(first_owner_names, first_owner_name_continued, second_owner_names)
    ]


def trust_name(overflow_series: pd.Series) -> List[str]:
    """
    Transformation for the trust column.

    :param overflow_series: a raw overflow name series.
    """
    return [
        name_overflow
        if ' TRUST' in name_overflow
        else ''
        for name_overflow in overflow_series.tolist()
    ]


def special_name_assessee(special_name_series: pd.Series) -> List[str]:
    """
    Transformations for the special name assessee column.

    :param special_name_series: Raw 'Special Name Assessee' column.
    """
    return [
        re.sub(
            r'\s+',
            ' ',
            special_name.
            replace('TR #', '').
            replace('C/O', '').
            replace('DBA', '').
            strip(),
        )
        for special_name in special_name_series.tolist()
    ]


def fractions(fraction_series: pd.Series) -> List[str]:
    """
    Transform the fraction column from timeseries to a fraction.

    :param fraction_series: a series of data that should be fractions.
    """
    return [
        '{0}/{1}'.format(str(fraction_value)[6], str(fraction_value)[9])
        if len(str(fraction_value)) > 3
        else ''
        for fraction_value in fraction_series.tolist()
    ]

def normalize_assessor(filepath: str) -> pd.DataFrame:
    """
    Reads in the dataset and returns a normalized dataframe.

    :param filepath: A csv assessor file.
    """
    usecols = [
        'AIN',
        'Agency Number',
        'Situs House No',
        'Fraction',
        'Direction',
        'Street Name',
        'Unit',
        'City State',
        'Zip',
        'Mail House No',
        'M Fraction',
        'M Direction',
        'M Street Name',
        'M Unit',
        'M City State',
        'M Zip',
        'Homeowner Exemption Val',
        'First Owner Name',
        'First Owner Name Overflow',
        'Special Name Legend',
        'Special Name Assessee',
        'Second Owner Name',
        'BD1 Year Built',
        'BD1 Units',
        'BD1 Bedrooms',
        'BD1 Baths',
        'BD1 Square Feet',
        'BD2 Year Built',
        'BD2 Units',
        'BD2 Bedrooms',
        'BD2 Baths',
        'BD2 Square Feet',
        'BD3 Year Built',
        'BD3 Units',
        'BD3 Bedrooms',
        'BD3 Baths',
        'BD3 Square Feet',
        'BD4 Year Built',
        'BD4 Units',
        'BD4 Bedrooms',
        'BD4 Baths',
        'BD4 Square Feet',
        'BD5 Year Built',
        'BD5 Units',
        'BD5 Bedrooms',
        'BD5 Baths',
        'BD5 Square Feet',
        'Landlord Reappraisal Year',
        'Landlord Units',
    ]
    dtype = {
        'Zip': 'string',
        'M Zip': 'string',
        'Fraction': 'string',
        'M Fraction': 'string',
        'Situs House No': 'string',
        'Mail House No': 'string',
        'Unit': 'string',
        'M Unit': 'string',
        'BD1 Year Built': 'int',
        'BD1 Units': 'int',
        'BD1 Bedrooms': 'int',
        'BD1 Baths': 'int',
        'BD1 Square Feet': 'int',
        'BD2 Year Built': 'int',
        'BD2 Units': 'int',
        'BD2 Bedrooms': 'int',
        'BD2 Baths': 'int',
        'BD2 Square Feet': 'int',
        'BD3 Year Built': 'int',
        'BD3 Units': 'int',
        'BD3 Bedrooms': 'int',
        'BD3 Baths': 'int',
        'BD3 Square Feet': 'int',
        'BD4 Year Built': 'int',
        'BD4 Units': 'int',
        'BD4 Bedrooms': 'int',
        'BD4 Baths': 'int',
        'BD4 Square Feet': 'int',
        'BD5 Year Built': 'int',
        'BD5 Units': 'int',
        'BD5 Bedrooms': 'int',
        'BD5 Baths': 'int',
        'BD5 Square Feet': 'int',
    }
    assessor_dataframe = pd.read_csv(
        filepath,
        usecols=usecols,
        dtype=dtype,
    )
    assessor_dataframe['Zip'] = [
        zip_[:5] for zip_ in assessor_dataframe['Zip'].tolist()
    ]
    assessor_dataframe['M Zip'] = [
        zip_[:5] for zip_ in assessor_dataframe['M Zip'].tolist()
    ]
    assessor_dataframe['Fraction'] = fractions(assessor_dataframe['Fraction']) 
    assessor_dataframe['M Fraction'] = fractions(assessor_dataframe['M Fraction'])
    assessor_dataframe[
        [
            'City',
            'State'
        ]
    ] = [
        ('', '') if len(city_state.strip().rsplit(' ', 1)) < 2 else
        itemgetter(0,1)(city_state.strip().rsplit(' ', 1))
        for city_state in assessor_dataframe['City State'].tolist()
    ]
    assessor_dataframe[
        [
            'M City',
            'M State'
        ]
    ] = [
        ('', '') if len(city_state.strip().rsplit(' ', 1)) < 2 else
        itemgetter(0,1)(city_state.strip().rsplit(' ', 1))
        for city_state in assessor_dataframe['M City State'].tolist()
    ]
    assessor_dataframe['Street Name'] = [
        street_name.strip() for street_name in assessor_dataframe['Street Name'].tolist()
    ]
    assessor_dataframe['M Street Name'] = [
        street_name.strip() for street_name in assessor_dataframe['M Street Name'].tolist()
    ]
    assessor_dataframe['Address1'] = (
        assessor_dataframe['Situs House No'] +
        assessor_dataframe['Fraction'] +
        assessor_dataframe['Direction'] +
        assessor_dataframe['Street Name']
    )
    assessor_dataframe['M Address1'] = (
        assessor_dataframe['Mail House No'] +
        assessor_dataframe['M Fraction'] +
        assessor_dataframe['M Direction'] +
        assessor_dataframe['M Street Name']
    )
    assessor_dataframe['names'] = owner_names(assessor_dataframe)
    assessor_dataframe['trust names'] = trust_name(assessor_dataframe['First Owner Name Overflow'])
    assessor_dataframe['Special Name Assessee'] = special_name_assessee(assessor_dataframe['Special Name Assessee'])

    assessor_dataframe.rename(
        columns={
            'Unit':'Address2',
            'Zip': 'Zipcode',
            'M Unit': 'M Address2',
            'M Zip': 'M Zipcode',
        },
        inplace=True,
    )
    assessor_dataframe['Zipcode'] = [
        0 if zip_.isdigit() == False else int(zip_)
        for zip_ in assessor_dataframe['Zipcode'].tolist()
    ]
    assessor_dataframe['M Zipcode'] = [
        0 if zip_.isdigit() == False else int(zip_)
        for zip_ in assessor_dataframe['M Zipcode'].tolist()
    ]
    assessor_dataframe['Address2'] = [
        '' if unit.strip() == '' else unit.strip()
        for unit in assessor_dataframe['Address2'].tolist()
    ]
    assessor_dataframe['M Address2'] = [
        '' if unit.strip() == '' else unit.strip()
        for unit in assessor_dataframe['M Address2'].tolist()
    ]
    assessor_dataframe.drop_duplicates(inplace=True)
    return assessor_dataframe

def process_assessor(filepath: str, session):
    """
    Transforms and inserts assessor data into the database.

    :param filepath: A csv assessor file.
    :param session: A SQLAlchemy session object.
    """
    assessor_dataframe = normalize_assessor(filepath)
    print('Start')
    for _, row in assessor_dataframe.iterrows():
        address_id = get_address_id(session, row)
        m_address = (
            session.query(AssessorMailing
).filter(
                AssessorMailing.address1 == row['M Address1'],
                AssessorMailing.address2 == row['M Address2'],
                AssessorMailing.city == row['M City'],
                AssessorMailing.state == row['M State'],
                AssessorMailing.zipcode == row['M Zipcode'],
            ).one_or_none()
        )
        # Need to wrap datatype.
        # Data was not being insered in some case do to diferent datatypes.
        if m_address is None:
            m_address = AssessorMailing(
                address1=str(row['M Address1']),
                address2=str(row['M Address2']),
                city=str(row['M City']),
                state=str(row['M State']),
                zipcode=int(row['M Zipcode']),
            )
            session.add(m_address)
            session.commit()
        assessor_entry = Assessor(
            address_id=address_id,
            assessor_mailing_id=m_address.assessor_mailing_id,
            ain=row['AIN'],
            agency_number=row['Agency Number'],
            special_name_assessee=row['Special Name Assessee'],
            special_name_legend=row['Special Name Legend'],
            names=row['names'],
            trust_name=row['trust names'],
            homeowner_expemtion_value=row['Homeowner Exemption Val'],
            landlord_reappraisal_year=row['Landlord Reappraisal Year'],
            landlord_units=row['Landlord Units'],
            baths_1=row['BD1 Baths'],
            bedrooms_1=row['BD1 Bedrooms'],
            square_feet_1=row['BD1 Square Feet'],
            units_1=row['BD1 Units'],
            year_1=row['BD1 Year Built'],
            baths_2=row['BD2 Baths'],
            bedrooms_2=row['BD2 Bedrooms'],
            square_feet_2=row['BD2 Square Feet'],
            units_2=row['BD2 Units'],
            year_2=row['BD2 Year Built'],
            baths_3=row['BD3 Baths'],
            bedrooms_3=row['BD3 Bedrooms'],
            square_feet_3=row['BD3 Square Feet'],
            units_3=row['BD3 Units'],
            year_3=row['BD3 Year Built'],
            baths_4=row['BD4 Baths'],
            bedrooms_4=row['BD4 Bedrooms'],
            square_feet_4=row['BD4 Square Feet'],
            units_4=row['BD4 Units'],
            year_4=row['BD4 Year Built'],
            baths_5=row['BD5 Baths'],
            bedrooms_5=row['BD5 Bedrooms'],
            square_feet_5=row['BD5 Square Feet'],
            units_5=row['BD5 Units'],
            year_5=row['BD5 Year Built'],
        )
        session.add(assessor_entry)
        session.commit()
        print('commited Assessor entry')
    print('Finished')


if __name__ == '__main__':
    multiple_files(
        filepath='',
        filetype='csv',
        process_function=process_assessor,
        session=SessionLocal(),
    )
