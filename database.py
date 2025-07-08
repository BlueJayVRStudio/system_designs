# POSTGRESQL
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

POSTGRES_ID = os.getenv("POSTGRES_ID")
POSTGRES_PW = os.getenv("POSTGRES_PW")
DB_HOST = os.getenv("PG_HOST")
DB_PORT = os.getenv("PG_PORT")
DB_NAME = os.getenv("PG_DB_NAME")

DATABASE_URL = f"postgresql://{POSTGRES_ID}:{POSTGRES_PW}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# MINIO
import boto3

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv("MINIO_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("MINIO_SECRET_KEY"),
    endpoint_url='http://192.168.50.249:9000',
    config=boto3.session.Config(signature_version='s3v4')
)