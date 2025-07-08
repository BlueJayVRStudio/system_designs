import boto3
from botocore.client import Config
import os
from dotenv import load_dotenv

load_dotenv()

# Init client
s3 = boto3.client(
    's3',
    aws_access_key_id=os.environ['MINIO_ACCESS_KEY'],
    aws_secret_access_key=os.environ['MINIO_SECRET_KEY'],
    endpoint_url=os.environ['MINIO_ENDPOINT'],
    config=Config(signature_version='s3v4')
)

# Use a single bucket or comma-separated list
# bucket_list = os.getenv('MINIO_BUCKET_NAME', 'videos').split(',')
bucket_list = ['publicbucket']

for bucket_name in bucket_list:
    bucket_name = bucket_name.strip()
    # print(f"Working on bucket: {bucket_name}")

    # Step 1: List and delete all objects
    try:
        while True:
            response = s3.list_objects_v2(Bucket=bucket_name)
            if 'Contents' not in response:
                break

            keys_to_delete = [{'Key': obj['Key']} for obj in response['Contents']]
            s3.delete_objects(Bucket=bucket_name, Delete={'Objects': keys_to_delete})
            # print(f"Deleted {len(keys_to_delete)} objects from {bucket_name}")

            if not response.get("IsTruncated"):
                break

        # Step 2: Delete bucket
        s3.delete_bucket(Bucket=bucket_name)
        # print(f"Deleted bucket: {bucket_name}")

    except Exception as e:
        # print(f"Failed to delete bucket '{bucket_name}': {e}")
        pass
