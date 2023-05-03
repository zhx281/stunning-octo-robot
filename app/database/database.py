import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

# Link engine to database
engine = create_engine(os.getenv("DATABASE_URI"))

# Create local session with engine
SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine)

Base = declarative_base()


# Calling the session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
