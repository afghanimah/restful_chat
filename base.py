from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# BACKUP_DATABASE_URL is where you can put your localhost db connection string for example.
# os.environ.get("DATABASE_URL") will get the connection string for the actual db from your hosting service.
# If you're running locally, the backup connection string will be used instead assuming
# that you don't haven't set DATABASE_URL yourself.
BACKUP_DATABASE_URL = "postgresql://localhost/restfulchat"
DATABASE_URL = os.environ.get("DATABASE_URL", BACKUP_DATABASE_URL)

engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)