"""
Purpose: Models for SQL Alchemy.

Author : Albert Ulysses <albertulysseschavez@gmail.com>
"""
# TODO: write docstrings for classes
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Index,
    Integer,
    String,
    Table,
)
from sqlalchemy.ext.declarative import declarative_base

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
            'zip',
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


class Platform(Base):
    __tablename__ = 'platform'

    platform_id = Column(Integer, primary_key=True)
    address_id = Column(ForeignKey('address.address_id'))
    listing_id = Column(String)
    listing_url = Column(String)
    host_id = Column(String)
    host_email = Column(String)
    registrant_number = Column(String)


class Builds(Base):
    __tablename__ = 'builds'

    build_id = Column(Integer, primary_key=True)
    build_number = Column(Integer)
    baths = Column(Integer)
    bedrooms = Column(Integer)
    square_feet = Column(Integer)
    units = Column(Integer)
    year = Column(Integer)


class AssessorMailing(Base):
    __tablename__ = 'assessor_mailing'

    assessor_mailing_id = Column(Integer, primary_key=True)
    address1 = Column(String)
    address2 = Column(String)
    city = Column(String)
    state = Column(String)
    zipcode = Column(Integer)

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


class RecipientMailing(Base):
    __tablename__ = 'recipient_mailing'

    recipient_mailing_id = Column(Integer, primary_key=True)
    address1 = Column(String)
    address2 = Column(String)
    city = Column(String)
    state = Column(String)
    zipcode = Column(Integer)


class Warnings(Base):
    __tablename__ = 'warnings'

    warning_id = Column(Integer, primary_key=True)
    address_id = Column(ForeignKey('address.address_id'))
    recipient_mailing_id = Column(ForeignKey('recipient_mailing.recipient_mailing_id'))
    parcel_number = Column(Integer)
    letter_number = Column(Integer)
    letter_type = Column(String)
    recipient_name = Column(String)
    date_of_letter = Column(String)


class Citation(Base):
    __tablename__ = 'citation'

    citation_id = Column(Integer, primary_key=True)
    warning_id = Column(ForeignKey('warnings.warning_id'))
    registration_number = Column(String)
    fine = Column(String)
    status = Column(String)
    violation = Column(String)


class Exempt(Base):
    __tablename__ = 'exempt'

    exempt_id = Column(Integer, primary_key=True)
    address_id = Column(ForeignKey('address.address_id'))
    host_apn = Column(String)
    exempt_type = Column(String)
    subtype = Column(String)


class HSOPlatforms(Base):
    __tablename__ = 'hso_platforms'

    hso_platforms_id = Column(Integer, primary_key=True)
    platforms = Column(String)

class HSORegistrant(Base):
    __tablename__ = 'hso_registrant'

    hso_registrant_id = Column(Integer, primary_key=True)
    address_id = Column(ForeignKey('address.address_id'))
    hso_platforms_id = Column(ForeignKey('hso_platforms.hso_platforms_id'))
    registration_number = Column(String)
    registrant_name = Column(String)
    generated_date = Column(String)


class HSORevocation(Base):
    __tablename__ = 'hso_revocation'

    hso_revocation_id = Column(Integer, primary_key=True)
    address_id = Column(ForeignKey('address.address_id'))
    registration_number = Column(String)
    registrant_name = Column(String)
    revoked_date = Column(String)


class HSODenials(Base):
    __tablename__ = 'hso_denials'

    hso_denials_id = Column(Integer, primary_key=True)
    address_id = Column(ForeignKey('address.address_id'))
    registrant_name = Column(String)
    application_date = Column(String)
    denial_date = Column(String)

# TODO: insert Airbnb tables
