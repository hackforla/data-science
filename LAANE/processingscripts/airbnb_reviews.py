"""
Purpose: To transform and insert Reviews datasets.

Author : Albert Ulysses <albertulysseschavez@gmail.com>
"""
import pandas as pd

from database.database import SessionLocal
from database.models import Reviews
from transformations.process_multiple_files import multiple_files


def normalize_reviews(filepath: str) -> pd.DataFrame:
    """
    Reads in the dataset and returns normalized dataframe.

    :param file: A file of Reviews data.
    """
    dtype = {
        'date': 'string',
        'reviewer_name': 'string',
        'comments': 'string',
    }
    reviews_dataframe = pd.read_csv(filepath, dtype=dtype)

    reviews_dataframe['listing_id'] = reviews_dataframe['listing_id'].fillna(0).astype('int64')
    reviews_dataframe['id'] = reviews_dataframe['id'].fillna(0).astype('int64')
    reviews_dataframe['reviewer_id'] = reviews_dataframe['reviewer_id'].fillna(0).astype('int64')
    reviews_dataframe.fillna('', inplace=True)
    reviews_dataframe.drop_duplicates(inplace=True)
    return reviews_dataframe


def process_reviews(filepath: str, session):
    """
    Transforms and inserts Reviews data into the database.

    :param filepath: A csv file of Reviews data.
    :param session: A SQLAlchemy session object.
    """
    reviews_dataframe = normalize_reviews(filepath)

    print('Start')
    for _, row in reviews_dataframe.iterrows():
        reviews_entry = (
            session.query(Reviews).filter(
                Reviews.review_id == row['id']
            ).one_or_none()
        )
        if reviews_entry is None:
            reviews_entry = Reviews(
                review_id=row['id'],
                airbnb_listing_id=row['listing_id'],
                reviewer_id=row['reviewer_id'],
                reviewer_name=row['reviewer_name'],
                date=row['date'],
                comments=row['comments'],
            )
            session.add(reviews_entry)
            session.commit()
        print('commited reviews_entry')


if __name__=='__main__':
    multiple_files(
        filepath='',
        filetype='csv',
        process_function=process_reviews,
        session=SessionLocal(),
    )
