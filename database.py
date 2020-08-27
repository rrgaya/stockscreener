import os
from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DB_USER = config("DB_USER")
DB_PASS = config("DB_PASS")
HOST = config("HOST")
PORT = config("PORT")
DBNAME = config("DBNAME")

# TODO
# DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{HOST}:{PORT}/{DBNAME}"

if "DATABASE_URL" in os.environ:
    ENV_DATABASE_URL = "postgres://ynrbxtwqegmste:58feea2c66eac7b672bc088ca20f50153320f9976896a52954af13e8aec90c74@ec2-34-224-229-81.compute-1.amazonaws.com:5432/d35so8n7e5oj21"
else:
    ENV_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/stocks"

engine = create_engine(ENV_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()