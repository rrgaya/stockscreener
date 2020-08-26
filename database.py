import databases
import sqlalchemy
from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DB_USER = config("DB_USER")
DB_PASS = config("DB_PASS")
HOST = config("HOST")
PORT = config("PORT")
DBNAME = config("DBNAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{HOST}:{PORT}/{DBNAME}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()