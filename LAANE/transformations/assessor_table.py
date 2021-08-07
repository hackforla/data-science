"""
Purpose: Transform assesor data to make Assessor table compatible.

Author : Albert Ulysses <albertulysseschavez@gmail.com>
"""

import numpy as np
import pandas as pd

# TODO: refactor to match WEMAKE STYLEGUIDE


def owner_names(assessor_dataframe: pd.DataFrame) -> pd.Series:
    """
    Transformations for the Owner Names column from a raw assesor dataframe.

    :param dataframe: a raw assessor dataframe.
    """
    first_owner_name_overflow = 'First Owner Name Overflow'

    assessor_dataframe['First Owner Name Clean'] = (
        assessor_dataframe['First Owner Name']
        .str.strip()
        .str.replace(',', ' ')
        .str.replace(' AND ', ' ')
        .str.replace(' AND', ' ')
        .str.replace(' TRS', '')
        .str.replace(' TR', '')
    )
    assessor_dataframe['First Owner Name Continued'] = np.where(
        assessor_dataframe[first_owner_name_overflow].str.contains(' TRUST') == False,
        assessor_dataframe[first_owner_name_overflow]
        .str.strip()
        .str.replace(',', ' ')
        .str.replace(' AND ', ' ')
        .str.replace(' AND', ' ')
        .str.replace(' TRS', '')
        .str.replace(' TR', ''),
        '',
    )
    assessor_dataframe['Second Owner Name Clean'] = (
        assessor_dataframe['Second Owner Name'].str.strip().str.replace(',', ' ')
    )
    assessor_dataframe['Owner Names'] = (
        assessor_dataframe['First Owner Name Clean']
        .str.cat(assessor_dataframe['First Owner Name Continued'], sep=' ', na_rep='')
        .str.cat(assessor_dataframe['Second Owner Name Clean'], sep=' ', na_rep='')
        .str.replace(r'\s+', ' ', regex=True)
        .str.strip()
    )

    return assessor_dataframe['Owner Names']


def trust_name(assessor_dataframe: pd.DataFrame) -> pd.Series:
    """
    Transformation for the trust column.

    :param assessor_dataframe: a raw assessor_dataframe.
    """

    assessor_dataframe["Trust Name"] = np.where(
        assessor_dataframe["First Owner Name Overflow"].str.contains(" TRUST") == True,
        assessor_dataframe["First Owner Name Overflow"],
        "",
    )
    return assessor_dataframe["Trust Name"]


def special_name_assessee(df: pd.DataFrame) -> pd.Series:
    """Special name assessee clean"""
    df["Special Name Assessee Clean"] = (
        df["Special Name Assessee"]
        .str.replace("DBA", "")
        .str.replace("C/O", "")
        .str.replace("TR #", "")
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )
    return df["Special Name Assessee Clean"]
