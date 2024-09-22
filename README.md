# Resume Matching Platform

## Giới thiệu

Resume Matching Platform là một ứng dụng web được xây dựng bằng Streamlit, cho phép người dùng tải lên hồ sơ và so sánh chúng với mô tả công việc. Ứng dụng sử dụng công nghệ AI để đánh giá và xếp hạng các hồ sơ dựa trên độ phù hợp với mô tả công việc, giúp cải thiện khả năng nhận hồ sơ của ứng viên.

## Tính năng

- Tải lên hồ sơ dưới dạng PDF và lưu trữ trên Amazon S3.
- Xếp hạng hồ sơ dựa trên độ phù hợp với mô tả công việc.
- Trích xuất thông tin từ hồ sơ và lưu trữ vào DynamoDB.
- Giao diện người dùng thân thiện và dễ sử dụng.

## Công nghệ sử dụng

- Streamlit
- Boto3 (AWS SDK for Python)
- Google Generative AI
- PyMuPDF (để xử lý PDF)
- Python Dotenv (để quản lý biến môi trường)

## Yêu cầu

- Python 3.7 trở lên
- Tài khoản AWS với quyền truy cập S3 và DynamoDB
- Tài khoản Google Cloud với API key cho Generative AI

## Hướng dẫn cài đặt và chạy

### 1. Clone repository

```bash
git clone https://github.com/yourusername/resume-matching-platform.git
cd resume-matching-platform
```

### 2. Tạo môi trường ảo (khuyến nghị)

```bash
python -m venv venv
source venv/bin/activate  # Trên macOS/Linux
venv\Scripts\activate  # Trên Windows
```

### 3. Cài đặt các phụ thuộc

```bash
pip install -r requirements.txt
```

### 4. Thiết lập biến môi trường

Tạo file .env trong thư mục gốc của dự án với nội dung sau:
```bash
GOOGLE_API_KEY=your_google_api_key
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
DYNAMODB_TABLE_NAME=your_dynamodb_table_name
```

### 5. Chạy ứng dụng

```bash
streamlit run app.py
```

Sau khi chạy lệnh trên, ứng dụng sẽ mở trong trình duyệt tại địa chỉ http://localhost:8501.

## Hướng dẫn sử dụng Docker

Nếu bạn muốn chạy ứng dụng bằng Docker, hãy làm theo các bước sau:
1. **Xây dựng hình ảnh Docker**: Chạy lệnh sau trong thư mục chứa Dockerfile:
```bash
docker build -t resume-matching-platform .
```
2. **Chạy container**: Sau khi xây dựng xong, bạn có thể chạy ứng dụng bằng lệnh:
```bash
docker run -p 8501:8501 resume-matching-platform
```
3. **Truy cập ứng dụng**: Mở trình duyệt và truy cập địa chỉ http://localhost:8501.

## Hướng dẫn sử dụng

1. **Tải lên hồ sơ**: Chọn tab "Upload CV to S3", nhập tên bucket S3 và tải lên hồ sơ PDF.
2. **Xếp hạng hồ sơ**: Chọn tab "Rank Candidates", tải lên hoặc chọn hồ sơ từ S3, sau đó nhập mô tả công việc và nhấn "Rank Candidates".
3. **Đánh giá HR**: Chọn tab "HR Evaluation", tải lên hồ sơ hoặc chọn từ S3, sau đó nhấn "Extract Information and Push to DynamoDB".

## Ghi chú

- Đảm bảo rằng các tài khoản AWS và Google Cloud của bạn đã được thiết lập đúng cách và có đủ quyền truy cập.
- Để biết thêm thông tin chi tiết về từng công nghệ sử dụng, hãy tham khảo tài liệu chính thức của chúng.

## Liên hệ

Nếu bạn có bất kỳ câu hỏi nào về dự án này, vui lòng liên hệ với tôi qua:
- Email: duonghiep59.it@gmail.com
- Linkedin: https://www.linkedin.com/in/duonghiepit/# resume-matching-platform
# resume-matching-platform
