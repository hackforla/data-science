"""
Purpose: To transform and insert AirbnbListings datasets.

Author : Albert Ulysses <albertulysseschavez@gmail.com>
"""
import re

import pandas as pd

from database.database import SessionLocal
from database.models import AirbnbListings, Hosts
from transformations.process_multiple_files import multiple_files


def normalize_listings(filepath: str) -> pd.DataFrame:
    """
    Reads in the dataset and returns normalized dataframe.

    :param file: A file of AirbnbListings data.
    """
    usecols = [
       'id',
       'listing_url',
       'scrape_id',
       'name',
       'description',
       'picture_url',
       'host_id',
       'host_url',
       'host_name',
       'host_since',
       'host_location',
       'host_is_superhost',
       'host_listings_count',
       'last_scraped',
       'neighbourhood_cleansed',
       'neighbourhood_group_cleansed',
       'latitude',
       'longitude',
       'property_type',
       'room_type',
       'price',
       'minimum_nights',
       'minimum_minimum_nights',
       'number_of_reviews',
       'number_of_reviews_ltm',
       'number_of_reviews_l30d',
       'first_review',
       'last_review',
       'license',
    ]
    dtype = {
        'listing_url': 'string',
        'name': 'string',
        'description': 'string',
        'picture_url': 'string',
        'host_url': 'string',
        'host_name': 'string',
        'host_since': 'string',
        'host_location': 'string',
        'host_is_superhost': 'string',
        'last_scraped': 'string',
        'neighbourhood_cleansed': 'string',
        'neighbourhood_group_cleansed': 'string',
        'latitude': 'float',
        'longitude': 'float',
        'property_type': 'string',
        'room_type': 'string',
        'price': 'string',
        'first_review': 'string',
        'last_review': 'string',
        'license': 'string',
    }

    listing_dataframe = pd.read_csv(
        filepath,
        usecols=usecols,
        dtype=dtype,
    )
    listing_dataframe['id'] = listing_dataframe['id'].fillna(0).astype('int64')
    listing_dataframe['scrape_id'] = listing_dataframe['scrape_id'].fillna(0).astype('int64')
    listing_dataframe['host_id'] = listing_dataframe['host_id'].fillna(0).astype('int64')
    listing_dataframe['host_listings_count'] = listing_dataframe['host_listings_count'].fillna(0).astype('int64')
    listing_dataframe['minimum_nights'] = listing_dataframe['minimum_nights'].fillna(0).astype('int64')
    listing_dataframe['minimum_minimum_nights'] = listing_dataframe['minimum_minimum_nights'].fillna(0).astype('int64')
    listing_dataframe['number_of_reviews'] = listing_dataframe['number_of_reviews'].fillna(0).astype('int64')
    listing_dataframe['number_of_reviews_ltm'] = listing_dataframe['number_of_reviews_ltm'].fillna(0).astype('int64')
    listing_dataframe['number_of_reviews_l30d'] = listing_dataframe['number_of_reviews_ltm'].fillna(0).astype('int64')
    listing_dataframe['latitude'] = listing_dataframe['latitude'].fillna(0).astype('float64')
    listing_dataframe['longitude'] = listing_dataframe['longitude'].fillna(0).astype('float64')
    listing_dataframe['price'] = [
         float(re.sub('[^0-9.]', '', price)) for price in listing_dataframe['price'].tolist()
    ]
    listing_dataframe.fillna('', inplace=True)
    listing_dataframe.drop_duplicates(inplace=True)
    return listing_dataframe


def process_listings(filepath: str, session):
    """
    Transforms and inserts AirbnbListings data into the database.

    :param filepath: A csv file of AirbnbListings data.
    :param session: A SQLAlchemy session object.
    """
    listing_dataframe = normalize_listings(filepath)

    print('Start')
    for _, row in listing_dataframe.iterrows():
        listing_entry = (
            session.query(AirbnbListings).filter(
                AirbnbListings.airbnb_listing_id == row['id']
            ).one_or_none()
        )
        if listing_entry is None:
            listing_entry = AirbnbListings(
                airbnb_listing_id=row['id'],
                host_id=row['host_id'],
                scrape_id=row['scrape_id'],
                name=row['name'],
                listing_url=row['listing_url'],
                license=row['license'],
                picture_url=row['picture_url'],
                description=row['description'],
                latitude=row['latitude'],
                longitude=row['longitude'],
                price=row['price'],
                first_review=row['first_review'],
                last_review=row['last_review'],
                neighbourhood_cleansed=row['neighbourhood_cleansed'],
                neighbourhood_groupd_cleansed=row['neighbourhood_group_cleansed'],
                property_type=row['property_type'],
                room_type=row['room_type'],
                minimum_minimum_nights=row['minimum_minimum_nights'],
                minimum_nights=row['minimum_nights'],
                number_of_reiews=row['number_of_reviews'],
                number_of_reiews_l30d=row['number_of_reviews_l30d'],
                number_of_reiews_ltm=row['number_of_reviews_ltm'],
                last_scraped=row['last_scraped'],
            )
            session.add(listing_entry)
            session.commit()
        if listing_entry.last_scraped < row['last_scraped']:
            (
                session.query(AirbnbListings).filter(
                    AirbnbListings.airbnb_listing_id == row['id']
                ).update(
                    {
                        'airbnb_listing_id': row['id'],
                        'host_id': row['host_id'],
                        'scrape_id': row['scrape_id'],
                        'name': row['name'],
                        'listing_url': row['listing_url'],
                        'license': row['license'],
                        'picture_url': row['picture_url'],
                        'description': row['description'],
                        'latitude': row['latitude'],
                        'longitude': row['longitude'],
                        'price': row['price'],
                        'first_review': row['first_review'],
                        'last_review': row['last_review'],
                        'neighbourhood_cleansed': row['neighbourhood_cleansed'],
                        'neighbourhood_groupd_cleansed': row['neighbourhood_group_cleansed'],
                        'property_type': row['property_type'],
                        'room_type': row['room_type'],
                        'minimum_minimum_nights': row['minimum_minimum_nights'],
                        'minimum_nights': row['minimum_nights'],
                        'number_of_reiews': row['number_of_reviews'],
                        'number_of_reiews_l30d': row['number_of_reviews_l30d'],
                        'number_of_reiews_ltm': row['number_of_reviews_ltm'],
                        'last_scraped': row['last_scraped'],
                    }
                )
            )
            session.commit()
        print('commited listing_entry')
        host_entry = (
            session.query(Hosts).filter(
                Hosts.host_id == row['host_id']
            ).one_or_none()
        )
        if host_entry is None:
            host_entry = Hosts(
                host_id=row['host_id'],
                host_name=row['host_name'],
                host_url=row['host_url'],
                host_since=row['host_since'],
                host_is_superhost=row['host_is_superhost'],
                host_location=row['host_location'],
                host_listings_count=row['host_listings_count'],
                last_scraped=row['last_scraped'],
            )
            session.add(host_entry)
            session.commit()
        if host_entry.last_scraped < row['last_scraped']:
            (
                session.query(Hosts).filter(
                    Hosts.host_id == row['host_id']
                ).update(
                    {
                        'host_name': row['host_name'],
                        'host_url': row['host_url'],
                        'host_since': row['host_since'],
                        'host_is_superhost': row['host_is_superhost'],
                        'host_location':row['host_location'],
                        'host_listings_count':row['host_listings_count'],
                        'last_scraped': row['last_scraped'],
                    }
                )
            )
            session.commit()
        print('commited host_entry')

    print('Finished')

if __name__ == '__main__':
    multiple_files(
        filepath='',
        filetype='csv',
        process_function=process_listings,
        session=SessionLocal(),
    )
