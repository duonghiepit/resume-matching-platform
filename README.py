readme = """
# Hướng Dẫn Sử Dụng / User Guide

## Tiếng Việt

### Giới Thiệu
Chào mừng bạn đến với nền tảng so khớp hồ sơ! Ứng dụng này giúp bạn tải lên CV, đánh giá các ứng viên dựa trên mô tả công việc, và trích xuất thông tin từ CV để lưu vào cơ sở dữ liệu.

### Các Chức Năng Chính

1. **Tải lên CV vào S3**
   - Nhập tên bucket S3 nơi bạn muốn lưu trữ các CV.
   - Chọn tệp CV (hỗ trợ định dạng PDF) từ máy tính của bạn.
   - Nhấn "Upload to S3" để tải lên.

2. **Xếp Hạng Ứng Viên**
   - Chọn nguồn cho CV: Tải từ máy tính hoặc từ S3.
   - Nếu tải từ máy tính, bạn sẽ cần chọn và tải lên CV.
   - Nếu chọn từ S3, bạn có thể lọc theo ngày và chọn các tệp CV cần xử lý.
   - Nhập mô tả công việc vào ô văn bản và nhấn "Rank Candidates" để xem xếp hạng của các ứng viên.

3. **Đánh Giá HR**
   - Tương tự như chức năng xếp hạng, bạn có thể tải lên hoặc chọn các CV từ S3.
   - Nhấn "Extract Information and Push to DynamoDB" để trích xuất thông tin từ CV và lưu vào DynamoDB.

4. **READ ME**
   - Tab này cung cấp hướng dẫn sử dụng cho người dùng về các chức năng của ứng dụng.

### Lưu Ý
- Đảm bảo rằng bạn đã cấu hình thông tin xác thực AWS và API trước khi sử dụng ứng dụng.
- Các tệp CV cần phải ở định dạng PDF.

---

## Tiếng Anh

### Introduction
Welcome to the Resume Matching Platform! This application helps you upload CVs, evaluate candidates based on job descriptions, and extract information from CVs to store in a database.

### Key Features

1. **Upload CV to S3**
   - Enter the S3 bucket name where you want to store the CVs.
   - Select CV files (PDF format supported) from your computer.
   - Click "Upload to S3" to upload.

2. **Rank Candidates**
   - Choose the source for resumes: Upload from Local or Source from S3.
   - If uploading from Local, select and upload your CVs.
   - If selecting from S3, you can filter by date and select the CV files to process.
   - Enter the job description in the text area and click "Rank Candidates" to see the ranking of candidates.

3. **HR Evaluation**
   - Similar to the ranking feature, you can upload or select CVs from S3.
   - Click "Extract Information and Push to DynamoDB" to extract information from the CVs and save it to DynamoDB.

4. **READ ME**
   - This tab provides user instructions for the functionalities of the application.

### Notes
- Ensure that you have configured your AWS credentials and API information before using the application.
- CV files should be in PDF format.
    """