import os
import boto3
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

# DynamoDB client
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name='ap-southeast-1'
)
