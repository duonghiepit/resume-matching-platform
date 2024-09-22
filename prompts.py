ATS_PROMPT_TEMPLATE = """
Hãy hành động như một hệ thống ATS (Application Tracking System) có kinh nghiệm cao hoặc chuyên môn sâu, với sự hiểu biết sâu sắc về lĩnh vực công nghệ, kỹ thuật phần mềm, khoa học dữ liệu, phân tích dữ liệu, và kỹ thuật dữ liệu lớn. Nhiệm vụ của bạn là đánh giá hồ sơ dựa trên mô tả công việc được cung cấp. Bạn cần xem xét rằng thị trường việc làm rất cạnh tranh và bạn nên cung cấp sự hỗ trợ tốt nhất để cải thiện hồ sơ. Hãy gán phần trăm phù hợp dựa trên JD và các từ khóa còn thiếu với độ chính xác cao.
resume: {resume}  
description: {jd}  
Tôi muốn phản hồi dưới dạng một chuỗi duy nhất có cấu trúc:  
{{"JD Match":"%", "MissingKeywords":[], "Profile Summary":""}}.
"""

HR_PROMPT_TEMPLATE = """
Hãy trích xuất các thông tin sau đây từ CV được cung cấp. Nếu một thông tin không có trong CV, hãy trả về "N/A" cho trường đó.
    Trả về kết quả dưới dạng một đối tượng JSON với các khóa sau:
    - HoTen: Họ và tên đầy đủ của ứng viên
    - Email: Địa chỉ email của ứng viên
    - SDT: Số điện thoại của ứng viên
    - NgaySinh: Ngày tháng năm sinh của ứng viên (định dạng DD/MM/YYYY nếu có)
    - DiaChi: Địa chỉ hiện tại của ứng viên
    - GioiThieuBanThan: Phần giới thiệu ngắn về bản thân ứng viên hoặc là mục tiêu nghề nghiệp
    - MangXaHoi: Danh sách các liên kết mạng xã hội (LinkedIn, GitHub, v.v.)
    - HocVan: Thông tin về quá trình học tập, bằng cấp
    - KinhNghiemLamViec: Chi tiết về kinh nghiệm làm việc trước đây
    - KyNang: Danh sách các kỹ năng chuyên môn và kỹ năng mềm
    - DuAn: Thông tin về các dự án đã tham gia hoặc thực hiện
resume: {resume}  
description: {jd}.
"""
