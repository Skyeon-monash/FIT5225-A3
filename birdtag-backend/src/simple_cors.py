#!/usr/bin/env python3
import os
from qcloud_cos import CosConfig, CosS3Client
from dotenv import load_dotenv

load_dotenv()

bucket = os.getenv("COS_BUCKET")
region = os.getenv("COS_REGION") 
secret_id = os.getenv("COS_SECRET_ID")
secret_key = os.getenv("COS_SECRET_KEY")

config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Scheme='https')
client = CosS3Client(config)

cors_config = {
    'CORSRule': [
        {
            'ID': 'birdtag-cors',
            'AllowedOrigin': ['http://localhost:5173', 'http://localhost:5174'],
            'AllowedMethod': ['PUT', 'GET', 'POST', 'DELETE', 'HEAD'],
            'AllowedHeader': ['*'],
            'ExposeHeader': ['ETag'],
            'MaxAgeSeconds': 300
        }
    ]
}

try:
    client.put_bucket_cors(Bucket=bucket, CORSConfiguration=cors_config)
    print("CORS configured successfully")
except Exception as e:
    print(f"Error: {e}")