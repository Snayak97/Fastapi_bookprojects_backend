from sqlalchemy import create_engine
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import Config

# postgraes
import psycopg2
from psycopg2.extras import RealDictCursor


# database connect
engine = create_engine(Config.DATABASE_URL)# normal



# session
SessionLocal = sessionmaker(bind=engine,autocommit=False,autoflush=False) # normal




# base declaration
Base = declarative_base()

# Check DB connection
def check_db_connection():
    try:
        # Try to connect to the database
        with engine.connect() as connection:
            print("Database connection successful!")
    except Exception as e:
        print(f"Database connection failed: {e}")

# Call the function to check the connection
check_db_connection()


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

