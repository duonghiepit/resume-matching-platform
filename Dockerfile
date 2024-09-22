# Sử dụng hình ảnh Python 3.10.14 chính thức
FROM python:3.10.14-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép file requirements.txt vào thư mục làm việc
COPY requirements.txt .

# Cài đặt các phụ thuộc
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào thư mục làm việc
COPY . .

# Thiết lập biến môi trường cho Streamlit
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_SERVER_ENABLE_XSRF=false

# Mở cổng 8501
EXPOSE 8501

# Chạy ứng dụng Streamlit
CMD ["streamlit", "run", "app.py"]
