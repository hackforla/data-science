"""
Purpose: Models for SQL Alchemy.

Author : Albert Ulysses <albertulysseschavez@gmail.com>
"""
# TODO: write docstrings for classes
from database.database import engine
from sqlalchemy import (
    Boolean,
    Column,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship

Base = declarative_base()


class Address(Base):
    __tablename__ = 'address'

    address_id = Column(Integer, primary_key=True)
    address1 = Column(String)
    address2 = Column(String)
    city = Column(String)
    state = Column(String)
    zipcode = Column(Integer)

    __table_args__ = (
        Index(
            'ix_address',
            'address1',
            'address2',
            'city',
            'state',
            'zipcode',
        ),
    )


class Tot(Base):
    __tablename__ = 'tot'

    tot_id = Column(Integer, primary_key=True)
    address_id = Column(ForeignKey('address.address_id'))
    legal_name = Column(String)
    dba_name = Column(String)
    cert_description = Column(String)
    location_start_date = Column(String)
    cer_effective_date = Column(String)

    address = relationship('Address', backref=backref('tot', order_by=tot_id))


class Platform(Base):
    __tablename__ = 'platform'

    platform_id = Column(Integer, primary_key=True)
    address_id = Column(ForeignKey('address.address_id'))
    listing_id = Column(String)
    listing_url = Column(String)
    host_id = Column(String)
    host_email = Column(String)
    registrant_number = Column(String)

    address = relationship(
        'Address',
        backref=backref('platform', order_by=platform_id),
    )


class Builds(Base):
    __tablename__ = 'builds'

    build_id = Column(Integer, primary_key=True)
    build_number = Column(Integer)
    baths = Column(Integer)
    bedrooms = Column(Integer)
    square_feet = Column(Integer)
    units = Column(Integer)
    year = Column(Integer)

    address = relationship(
        'Assessor',
        backref=backref('builds', order_by=build_id),
    )


class AssessorMailing(Base):
    __tablename__ = 'assessor_mailing'

    assessor_mailing_id = Column(Integer, primary_key=True)
    address1 = Column(String)
    address2 = Column(String)
    city = Column(String)
    state = Column(String)
    zipcode = Column(Integer)

    address = relationship(
        'Assessor',
        backref=backref('assessor_mailing', order_by=assessor_mailing_id),
    )

    __table_args__ = (
        Index(
            'ix_assessor_mailing',
            'address1',
            'address2',
            'city',
            'state',
            'zipcode',
        ),
    )


class Assessor(Base):
    __tablename__ = 'assessor'

    assessor_id = Column(Integer, primary_key=True)
    address_id = Column(ForeignKey('address.address_id'))
    build_id = Column(ForeignKey('builds.build_id'))
    assessor_mailing_id = Column(
        ForeignKey('assessor_mailing.assessor_mailing_id'),
    )
    ain = Column(String)
    agency_number = Column(Integer)
    special_name_assessee = Column(String)
    special_name_legend = Column(String)
    names = Column(String)
    trust_name = Column(String)
    homeowner_expemtion_value = Column(Integer)
    landlord_reappraisal_year = Column(Integer)
    landlord_units = Column(Integer)

    address = relationship(
        'Address',
        backref=backref('assessor', order_by=assessor_id),
    )


class Complaints(Base):
    __tablename__ = 'complaints'
    complaints_id = Column(Integer, primary_key=True)
    address_id = Column(ForeignKey('address.address_id'))
    registration_number = Column(String)
    complaint_type = Column(String)
    call_time = Column(String)
    call_date = Column(String)
    caller_name = Column(String)
    reported_issue = Column(String)

    address = relationship(
        'Address',
        backref=backref('complaints', order_by=complaints_id),
    )


class CategoricallyIneligible(Base):
    __tablename__ = 'categorically_ineligible'

    categorically_ineligible_id = Column(Integer, primary_key=True)
    address_id = Column(ForeignKey('address.address_id'))
    entire_building = Column(Boolean)
    mixed_income = Column(Boolean)
    ellis_act = Column(Boolean)
    income_restrict = Column(Boolean)
    req_blacklist = Column(Boolean)
    rso = Column(Boolean)
    prohibited = Column(Boolean)

    address = relationship(
        'Address',
        backref=backref(
            'categorically_ineligible',
            order_by=categorically_ineligible_id,
        ),
    )


class Noncompliant(Base):
    __tablename__ = 'noncompliant'

    noncompliant_id = Column(Integer, primary_key=True)
    address_id = Column(ForeignKey('address.address_id'))
    parcel_number = Column(Integer)
    permit_number = Column(String)
    case_number = Column(String)
    listing_url = Column(String)
    listing_title = Column(String)
    listing_property_type = Column(String)
    listing_room_type = Column(String)
    land_use = Column(String)
    compliance_explanation = Column(String)
    date_generated = Column(String)

    address = relationship(
        'Address',
        backref=backref('noncompliant', order_by=noncompliant_id),
    )


class RecipientMailing(Base):
    __tablename__ = 'recipient_mailing'

    recipient_mailing_id = Column(Integer, primary_key=True)
    address1 = Column(String)
    address2 = Column(String)
    city = Column(String)
    state = Column(String)
    zipcode = Column(Integer)

    warnings = relationship(
        'Warnings',
        backref=backref('recipient_mailing', order_by=recipient_mailing_id),
    )


class Citation(Base):
    __tablename__ = 'citation'

    citation_id = Column(Integer, primary_key=True)
    warning_id = Column(ForeignKey('warnings.warning_id'))
    registration_number = Column(String)
    fine = Column(String)
    status = Column(String)
    violation = Column(String)

    warnings = relationship(
        'Warnings',
        backref=backref('citation', order_by=citation_id),
    )


class Warnings(Base):
    __tablename__ = 'warnings'

    warning_id = Column(Integer, primary_key=True)
    address_id = Column(ForeignKey('address.address_id'))
    recipient_mailing_id = Column(
        ForeignKey('recipient_mailing.recipient_mailing_id'),
    )
    parcel_number = Column(Integer)
    letter_number = Column(Integer)
    letter_type = Column(String)
    recipient_name = Column(String)
    date_of_letter = Column(String)

    address = relationship(
        'Address',
        backref=backref('warnings', order_by=warning_id),
    )


class Exempt(Base):
    __tablename__ = 'exempt'

    exempt_id = Column(Integer, primary_key=True)
    address_id = Column(ForeignKey('address.address_id'))
    host_apn = Column(String)
    exempt_type = Column(String)
    subtype = Column(String)

    address = relationship(
        'Address',
        backref=backref('exempt', order_by=exempt_id),
    )


class HSOPlatforms(Base):
    __tablename__ = 'hso_platforms'

    hso_platforms_id = Column(Integer, primary_key=True)
    platforms = Column(String)

    hso_registrant = relationship(
        'HSORegistrant',
        backref=backref('hso_platforms', order_by=hso_platforms_id),
    )

class HSORegistrant(Base):
    __tablename__ = 'hso_registrant'

    hso_registrant_id = Column(Integer, primary_key=True)
    address_id = Column(ForeignKey('address.address_id'))
    hso_platforms_id = Column(ForeignKey('hso_platforms.hso_platforms_id'))
    registration_number = Column(String)
    registrant_name = Column(String)
    generated_date = Column(String)

    address = relationship(
        'Address',
        backref=backref('hso_registrant', order_by=hso_registrant_id),
    )


class HSORevocation(Base):
    __tablename__ = 'hso_revocation'

    hso_revocation_id = Column(Integer, primary_key=True)
    address_id = Column(ForeignKey('address.address_id'))
    registration_number = Column(String)
    registrant_name = Column(String)
    revoked_date = Column(String)

    address = relationship(
        'Address',
        backref=backref('hso_revocation', order_by=hso_revocation_id),
    )


class HSODenials(Base):
    __tablename__ = 'hso_denials'

    hso_denials_id = Column(Integer, primary_key=True)
    address_id = Column(ForeignKey('address.address_id'))
    registrant_name = Column(String)
    application_date = Column(String)
    denial_date = Column(String)

    address = relationship(
        'Address',
        backref=backref('hso_denials', order_by=hso_denials_id),
    )


class Reviews(Base):
    __tablename__ = 'reviews'

    review_id = Column(Integer, primary_key=True)
    airbnb_listing_id = Column(ForeignKey('airbnb_listings.airbnb_listing_id'))
    reviewer_id = Column(Integer)
    reviewer_name = Column(String)
    date = Column(String)
    comments = Column(String)

    airbnb_listing = relationship(
        'AirbnbListings',
        backref=backref('reviews', order_by=review_id),
    )

class Hosts(Base):
    __tablename__ = 'hosts'

    host_id = Column(Integer, primary_key=True)
    host_name = Column(String)
    host_url = Column(String)
    host_since = Column(String)
    host_is_superhost = Column(Boolean)
    host_location = Column(String)
    host_listings_count = Column(Integer)

    airbnb_listing = relationship(
        'AirbnbListings',
        backref=backref('hosts', order_by=host_id),
    )


class AirbnbListings(Base):
    __tablename__ = 'airbnb_listings'

    airbnb_listing_id = Column(Integer, primary_key=True)
    host_id = Column(ForeignKey('hosts.host_id'))
    scrape_id = Column(Integer)
    name = Column(String)
    listing_url = Column(String)
    license = Column(String)
    picture_url = Column(String)
    description = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    price = Column(Float)
    first_review = Column(String)
    last_review = Column(String)
    neighbourhood_cleansed = Column(String)
    neighbourhood_groupd_cleansed = Column(String)
    property_type = Column(String)
    room_type = Column(String)
    minimum_minimum_nights = Column(Integer)
    minimum_nights = Column(Integer)
    number_of_reiews = Column(Integer)
    number_of_reiews_l30d = Column(Integer)
    number_of_reiews_ltm = Column(Integer)

Base.metadata.create_all(bind=engine)
