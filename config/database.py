import os
from sqlmodel import create_engine, Session
# from sqlalchemy.orm.session import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base

sqlite_file_name = "database.sqlite"
# base_dir = os.path.dirname(os.path.realpath(__file__))

# database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

session = Session(engine)

# Base = declarative_base()