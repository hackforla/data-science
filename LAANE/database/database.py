"""
Purpose: Connecting to the database.

Author : Albert Ulysses <albertulysseschavez@gmail.com>
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# unhash below when testing
# SQLALCHEMY_DATABASE_URL = 'sqlite:///./LAANEtest.db'
# SQLALCHEMY_DATABASE_URL = 'sqlite:///./LAANE.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
