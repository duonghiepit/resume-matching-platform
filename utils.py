import streamlit as st
import google.generativeai as genai
import os
import boto3
import fitz  # PyMuPDF
import re
import json
from botocore.exceptions import ClientError
from prompts import ATS_PROMPT_TEMPLATE, HR_PROMPT_TEMPLATE

# Load environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

# DynamoDB client
dynamodb = boto3.resource('dynamodb',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name='ap-southeast-1'  # Replace with your AWS region
)

def push_to_dynamodb(table_name, data):
    table = dynamodb.Table(table_name)
    try:
        response = table.put_item(Item=data)
        return response
    except ClientError as e:
        st.error(f"Error pushing data to DynamoDB: {e.response['Error']['Message']}")
        return None

def upload_file_to_s3(file, bucket_name, object_name=None):
    if object_name is None:
        object_name = file.name
    try:
        s3_client.upload_fileobj(file, bucket_name, object_name)
        return True
    except Exception as e:
        st.error(f"Error uploading file to S3: {e}")
        return False

def get_gemini_response(prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    if not response or not response.text.strip():
        st.error("Received an empty response from the Gemini API.")
        return None
    return response.text

def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

def clean_and_preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s\.\,\;\:\-]", "", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[\*\•]", "-", text)
    return text

def create_prompt(template, resume_text, jd_text):
    return template.format(resume=resume_text, jd=jd_text)

def calculate_jd_score(resume_text, jd_text):
    prompt = create_prompt(ATS_PROMPT_TEMPLATE, resume_text, jd_text)
    response = get_gemini_response(prompt)

    jd_match = 0
    missing_keywords = []
    profile_summary = ""
    if response is None:
        return jd_match, missing_keywords, profile_summary

    try:
        response_dict = json.loads(response)
        jd_match = float(response_dict["JD Match"].strip('%'))
        missing_keywords = response_dict.get("MissingKeywords", [])
        profile_summary = response_dict.get("Profile Summary", "")
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON response: {e}. Response was: {response}")
    except KeyError as e:
        st.error(f"Missing expected key in response: {e}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")
    return jd_match, missing_keywords, profile_summary

def list_files_in_s3(bucket_name):
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        return [item['Key'] for item in response.get('Contents', [])]
    except Exception as e:
        st.error(f"Error retrieving files from S3: {e}")
        return []

def get_gemini_response_4_extract(prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)

    response = response.text
    json_str = response.replace('```', '')
    json_start_index = json_str.find('{')

    if json_start_index != -1:
        json_str = json_str[json_start_index:]

    return json_str

def process_rank_candidates(resume_texts, jd, top_k):
    results = {}
    for resume_name, resume_text in resume_texts.items():
        match_score, missing_keywords, profile_summary = calculate_jd_score(resume_text, jd)
        results[resume_name] = {
            "score": match_score,
            "missing_keywords": missing_keywords,
            "profile_summary": profile_summary
        }

    sorted_results = sorted(results.items(), key=lambda x: x[1]["score"], reverse=True)
    top_k_results = sorted_results[:top_k]

    return top_k_results

def process_hr_evaluation(resume_texts):
    extracted_info = {}
    for resume_name, resume_text in resume_texts.items():
        prompt = create_prompt(HR_PROMPT_TEMPLATE, resume_text, None)
        json_response = get_gemini_response_4_extract(prompt)

        try:
            extracted_info[resume_name] = json.loads(json_response)
        except json.JSONDecodeError as e:
            st.error(f"Error decoding JSON response for {resume_name}: {e}")

    return extracted_info

def get_next_resume_id():
    tracker_table = dynamodb.Table('ResumeIDTracker')
    try:
        response = tracker_table.update_item(
            Key={'ID': 'resumeID'},
            UpdateExpression='SET CurrentValue = if_not_exists(CurrentValue, :start) + :inc',
            ExpressionAttributeValues={
                ':inc': 1,
                ':start': 0  # Default starting value if CurrentValue doesn't exist
            },
            ReturnValues="UPDATED_NEW"
        )
        return response['Attributes']['CurrentValue']
    except ClientError as e:
        st.error(f"Error getting next resumeID: {e.response['Error']['Message']}")
        return None

def list_files_with_metadata(bucket_name):
    s3_client = boto3.client('s3')
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    
    files_with_metadata = []
    
    if 'Contents' in response:
        for obj in response['Contents']:
            file_info = {
                'Key': obj['Key'],
                'LastModified': obj['LastModified'],
                'Size': obj['Size']  # You can include other metadata if needed
            }
            files_with_metadata.append(file_info)

    return files_with_metadata