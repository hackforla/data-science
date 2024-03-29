"""
Purpose: Reusable code for SQLAlchemy.

Author: Albert Ulysses <albertulysseschavez@gmail.com>
"""
# TODO: write integration test for the function.
# Test isn't written at the moment because needs mock db.
from database.models import Address


def get_address_id(session, row) -> int:
    """
    Gets an id or creates and returns id if doesn't exist.

    :param session: A SQLAlchemy session object.
    :param row: a Pandas DataFrame row.
    """
    address = (
        session.query(Address).filter(
            Address.address1 == row['Address1'],
            Address.address2 == row['Address2'],
            Address.city == row['City'],
            Address.state == row['State'],
            Address.zipcode == row['Zipcode'],
        ).one_or_none()
    )
    # Need to wrap datatype.
    # Data was not being insered in some case do to diferent datatypes.
    if address is None:
        address = Address(
            address1=str(row['Address1']),
            address2=str(row['Address2']),
            city=str(row['City']),
            state=str(row['State']),
            zipcode=int(row['Zipcode']),
        )
        session.add(address)
        session.commit()
    return address.address_id
