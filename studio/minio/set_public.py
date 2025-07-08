import boto3
from botocore.client import Config
import os
import json
from dotenv import load_dotenv

# Load from .env file (optional)
load_dotenv()

# Read values from environment
s3 = boto3.client(
    's3',
    aws_access_key_id=os.environ['MINIO_ACCESS_KEY'],
    aws_secret_access_key=os.environ['MINIO_SECRET_KEY'],
    endpoint_url=os.environ['MINIO_ENDPOINT'],
    config=Config(signature_version='s3v4')
)

# bucket_name = os.environ.get('MINIO_BUCKET_NAME', 'videos')
bucket_name = 'publicbucket'

# Public read-only bucket policy
policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": ["s3:GetObject"],
            "Resource": [f"arn:aws:s3:::{bucket_name}/*"]
        }
    ]
}

# Apply policy
s3.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(policy))
print(f"Public read-only policy applied to bucket '{bucket_name}'")
