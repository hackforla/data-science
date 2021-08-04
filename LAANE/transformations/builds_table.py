#!/usr/bin/env python3
"""
Purpose: To transform Assessor data to be Build Table Compatible.

Author : Albert Ulysses <albertulysseschavez@gmail.com>
"""
from typing import Literal

import pandas as pd

# ignore warning for Build Number column - False Negative
pd.options.mode.chained_assignment = None


def builds(assessor_dataframe: pd.DataFrame, build_number: Literal[1, 2, 3, 4, 5]) -> pd.DataFrame:
    """
    Transforms the assessor dataframe into a build dataframe.

    :param assessor_dataframe: A raw assessor dataframe.
    :param build_number: The build number.
    """
    column_beginning = 'BD{0}'.format(build_number)
    build_dataframe = assessor_dataframe[[
        '{0} Baths'.format(column_beginning),
        '{0} Bedrooms'.format(column_beginning),
        '{0} Square Feet'.format(column_beginning),
        '{0} Units'.format(column_beginning),
        '{0} Year Built'.format(column_beginning),
    ]]
    build_dataframe.columns = [
        'Baths',
        'Bedrooms',
        'Square Feet',
        'Units',
        'Year Built',
    ]

    build_dataframe['Build Number'] = build_number
    return build_dataframe


def main():
    """
    TODO: write code that allows you to pass an excel file and
    returns transformed csv files saved as 10 chunk files.

    """
    pass


if __name__ == '__main__':
    main()
