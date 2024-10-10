import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Thông tin cấu hình email
smtp_server = "smtp.zoho.com"
port = 465  # Sử dụng cổng 465 cho SSL
sender_email = "thongtin.dathang@tannacompany.org"  # Địa chỉ email Zoho của bạn
password = "Suongnguyen83@"  # Mật khẩu của bạn
receiver_email = "phanvokhanhtrang54@gmail.com"  # Địa chỉ email người nhận

# Tạo nội dung email
subject = "Kiểm tra tính năng đặt hàng - khánh trang"
body = "đây là email được gửi bởi Phan Công Dũng để kiểm tra tính năng"

# Tạo email
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["test"] = subject
message.attach(MIMEText(body, "plain"))

# Kết nối với máy chủ SMTP và gửi email
try:
    with smtplib.SMTP_SSL(smtp_server, port) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
