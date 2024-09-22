import streamlit as st
import os

from utils import (
    push_to_dynamodb,
    upload_file_to_s3,
    extract_text_from_pdf,
    clean_and_preprocess_text,
    process_rank_candidates,
    process_hr_evaluation,
    get_next_resume_id,
    list_files_in_s3,
    list_files_with_metadata
)
from dotenv import load_dotenv
from README import readme
from config import s3_client


# Load environment variables
load_dotenv()

# Streamlit App
st.set_page_config(page_title="Resume Matching Platform", layout="wide")

st.title("Resume Matching Platform")
st.text("Improve Your Resume ATS")

# Create tabs
tabs = st.tabs(["Upload CV to S3", "Rank Candidates", "HR Evaluation", "READ ME"])

# READ ME Instructions
with tabs[3]:
    st.header("User Guide")
    st.write(readme)

# To store S3 files
s3_files = []

with tabs[0]:
    st.header("Upload CV to S3")
    bucket_name = st.text_input("Enter S3 Bucket Name", "inda-resume-bucket")
    uploaded_files = st.file_uploader("Choose CV files", accept_multiple_files=True, type=['pdf'])

    if uploaded_files:
        if st.button("Upload to S3"):
            for file in uploaded_files:
                if upload_file_to_s3(file, bucket_name):
                    st.success(f"Successfully uploaded {file.name} to S3 bucket {bucket_name}")
                else:
                    st.error(f"Failed to upload {file.name}")

# Rank Candidates tab
with tabs[1]:
    st.subheader("Rank Candidates")
    source_option = st.radio("Choose source for resumes:", ["Upload from Local", "Source from S3"], key="source_option_rank")

    if "resume_texts" not in st.session_state:
        st.session_state.resume_texts = {}

    if source_option == "Upload from Local":
        uploaded_files = st.file_uploader("Upload Your Resume", type="pdf", accept_multiple_files=True, help="Please upload the PDF", key="upload_rank")
        if uploaded_files:
            for uploaded_file in uploaded_files:
                resume_text = extract_text_from_pdf(uploaded_file)
                st.session_state.resume_texts[uploaded_file.name] = clean_and_preprocess_text(resume_text)
            st.success(f"Processed {len(uploaded_files)} files")

    else:
        bucket_name = st.text_input("Enter S3 Bucket Name", "inda-resume-bucket", key="bucket_name_rank")

        # Date filter inputs
        start_date = st.date_input("Start Date", value=None, key="start_date_rank")
        end_date = st.date_input("End Date", value=None, key="end_date_rank")

        if st.button("Get Files from S3"):
            s3_files_with_metadata = list_files_with_metadata(bucket_name)
            filtered_files = [
                file['Key'] for file in s3_files_with_metadata
                if (start_date is None or file['LastModified'].date() >= start_date) and
                   (end_date is None or file['LastModified'].date() <= end_date)
            ]

            if not filtered_files:
                st.warning("No files match the date filter.")
            else:
                st.session_state.s3_files_loaded = True
                st.session_state.filtered_files = filtered_files
                st.success(f"Found {len(filtered_files)} files matching the criteria")

        if getattr(st.session_state, 's3_files_loaded', False):
            select_all = st.checkbox("Select All", key="select_all_s3")

            # Update selection based on "Select All" checkbox
            if select_all:
                st.session_state.selected_files_s3 = st.session_state.filtered_files
            else:
                st.session_state.selected_files_s3 = st.multiselect("Select files from S3", st.session_state.filtered_files, key="select_files_s3")
            
            if st.session_state.selected_files_s3:
                if st.button("Process Selected S3 Files"):
                    for file in st.session_state.selected_files_s3:
                        response = s3_client.get_object(Bucket=bucket_name, Key=file)
                        resume_text = extract_text_from_pdf(response['Body'])
                        st.session_state.resume_texts[file] = clean_and_preprocess_text(resume_text)
                    st.success(f"Processed {len(st.session_state.selected_files_s3)} files from S3")

    # Check if resumes were processed
    if st.session_state.resume_texts:
        st.write(f"Total resumes processed: {len(st.session_state.resume_texts)}")
        jd_text = st.text_area("Paste Job Description", height=200)
        top_k = st.slider("Number of Top Resumes to Display", 1, len(uploaded_files) if source_option == "Upload from Local" else len(st.session_state.resume_texts), 1)

        # Process button to rank candidates
        if st.button("Rank Candidates"):
            if jd_text:
                top_candidates = process_rank_candidates(st.session_state.resume_texts, jd_text, top_k)
                st.subheader("Top Candidates")
                for candidate, details in top_candidates:
                    st.write(f"{candidate}: {details['score']}% match")
                    st.write(f"Missing Keywords: {', '.join(details['missing_keywords'])}")
                    st.write(f"Profile Summary: {details['profile_summary']}")
                    st.write("-----------------------------------------------------------------------")
            else:
                st.error("Please enter a job description.")
    else:
        st.warning("No resumes processed yet. Please upload or select resumes from S3.")

# HR Evaluation tab
with tabs[2]:
    st.subheader("HR Evaluation")
    source_option = st.radio("Choose source for resumes:", ["Upload from Local", "Source from S3"], key="source_option_eval")
    
    resume_texts = {}

    if source_option == "Upload from Local":
        uploaded_files = st.file_uploader("Upload Your Resume", type="pdf", accept_multiple_files=True, help="Please upload the PDF", key="upload_eval")
        if uploaded_files:
            for uploaded_file in uploaded_files:
                resume_text = extract_text_from_pdf(uploaded_file)
                resume_texts[uploaded_file.name] = clean_and_preprocess_text(resume_text)
    else:
        bucket_name = st.text_input("Enter S3 Bucket Name", "inda-resume-bucket", key="bucket_name_eval")
        if st.button("Get Files from S3"):
            s3_files = list_files_in_s3(bucket_name)

        if s3_files:
            selected_files = st.multiselect("Select files from S3", s3_files)
            if selected_files:
                for selected_file in selected_files:
                    response = s3_client.get_object(Bucket=bucket_name, Key=selected_file)
                    resume_text = extract_text_from_pdf(response['Body'])
                    resume_texts[selected_file] = clean_and_preprocess_text(resume_text)

    if resume_texts:
        if st.button("Extract Information and Push to DynamoDB"):
            extracted_info = process_hr_evaluation(resume_texts)
            st.subheader("Extracted Information")
            for resume_name, info in extracted_info.items():
                st.write(f"Information for {resume_name}:")
                
                # Get the next resumeID
                resumeID = get_next_resume_id()
                if resumeID is not None:
                    # Push to DynamoDB
                    data_to_push = {
                        "resumeID": resumeID,
                    } | info
                    response = push_to_dynamodb(os.getenv("DYNAMODB_TABLE_NAME"), data_to_push)
                    if response:
                        st.success(f"Successfully pushed data for {resume_name} to DynamoDB")
                    else:
                        st.error(f"Failed to push data for {resume_name} to DynamoDB")
