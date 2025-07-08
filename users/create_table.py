from sqlalchemy import Column, String, Integer, DateTime, Boolean, create_engine
from sqlalchemy.orm import declarative_base
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

POSTGRES_ID = os.getenv("POSTGRES_ID")
POSTGRES_PW = os.getenv("POSTGRES_PW")
DB_HOST = os.getenv("PG_HOST")
DB_PORT = os.getenv("PG_PORT")
DB_NAME = os.getenv("PG_DB_NAME")

DATABASE_URL = f"postgresql://{POSTGRES_ID}:{POSTGRES_PW}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

Base = declarative_base()
engine = create_engine(DATABASE_URL)

class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True, index=True)  # index for performance
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=True)  # store hashed password
    created_at = Column(DateTime, default=datetime.utcnow)
    email_verified = Column(Boolean, default=False)
    version = Column(Integer, default=1)

if __name__ == "__main__":
    print(f"Creating tables in {DB_NAME}...")
    Base.metadata.create_all(bind=engine)
    print("Done.")