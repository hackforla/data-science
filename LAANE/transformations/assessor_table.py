# TODO: make the files executable
"""
Purpose: To transform and normalize Assessor data into simpler CSV files.

Author : Albert Ulysses <albertulysseschavez@gmail.com>
"""
import re
from typing import List

import pandas as pd


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

# TODO: write main function that returns csv files that are normalized
