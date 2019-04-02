from sqlalchemy import create_engine
from base import Base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.environ['DATABASE_URL']

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)