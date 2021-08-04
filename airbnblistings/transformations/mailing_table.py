#!/usr/bin/env python3
"""
Purpose: To transform Assessor data to be Mailing Table compatible.

Author : Albert Ulysses <albertulysseschavez@gmail.com>
"""
from typing import List

import numpy as np
import pandas as pd


def state(city_state_series: pd.Series, states: List[str]) -> pd.Series:
    """
    Transforms the city state column of the assessor table into a State.

    :param city_state_series: the City State series of raw Assessor dataframe.
    """
    state_sub_string = city_state_series.str.strip().str[-2:]
    state_values = np.where(
        state_sub_string.str.contains('|'.join(states)),
        state_sub_string,
        np.nan,
    )
    return pd.Series(state_values, name='State')
