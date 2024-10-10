import time
import smtplib
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# Cấu hình SMTP
SMTP_SERVER = "smtp.zoho.com"
SMTP_PORT = 465
SMTP_USER = "thongtin.dathang@tannacompany.org"
SMTP_PASSWORD = "Suongnguyen83@"

# Tệp xác thực Google API
SERVICE_ACCOUNT_FILE = 'qhh2310-a6b410fe6054.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# ID của Google Sheet (cần thay bằng ID của bạn)
SPREADSHEET_ID = '1axbUoChS62_k8fpLcxX5G20lwpC3xUyo1J8-c2h_5fc'
RANGE_NAME = 'sheet1'  # Không chỉ định cột cụ thể, get toàn bộ sheet

# Xác thực Google Sheets API
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)

# Lưu trạng thái đơn hàng cũ để so sánh
previous_orders = {}

# Hàm gửi email
def send_email(subject, body, to_email):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SMTP_USER
    msg['To'] = to_email

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, to_email, msg.as_string())

# Hàm lấy dữ liệu từ Google Sheet
def get_google_sheet_data():
    sheet = service.spreadsheets()
    # Lấy toàn bộ dữ liệu
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    rows = result.get('values', [])
    return rows

# Hàm xử lý đơn hàng
def process_orders():
    global previous_orders

    rows = get_google_sheet_data()

    # Bỏ qua hàng tiêu đề
    for i, row in enumerate(rows[1:], start=2):
        # Chỉ lấy các cột cần thiết
        timestamp = row[0] if len(row) > 0 else ''
        score = row[1] if len(row) > 1 else ''
        name = row[2] if len(row) > 2 else ''
        email = row[3] if len(row) > 3 else ''
        class_name = row[4] if len(row) > 4 else ''
        phone_number = row[5] if len(row) > 5 else ''
        facebook_name = row[6] if len(row) > 6 else ''
        order_details = row[7] if len(row) > 7 else ''
        notes = row[8] if len(row) > 8 else ''
        
        # Lấy trạng thái "Đã xác nhận đơn", "Đang giao" và "Đã giao"
        confirm_status = row[9] if len(row) > 9 else ''
        shipping_status = row[10] if len(row) > 10 else ''  # Cột "Đang Giao"
        delivery_status = row[11] if len(row) > 11 else ''  # Cột "Đã Giao"
        
        # Kiểm tra đơn hàng mới (chưa có trong danh sách cũ)
        if email not in previous_orders:
            # Gửi email đơn hàng mới
            subject = f"Đơn hàng của {name} tại 10 TIN 1 Quốc Học Huế đã được ghi nhận."
            body = f"""Cảm ơn quý khách đã đặt hàng tại 10 TIN 1.
Đơn đặt hàng của quý đã được chúng tôi ghi nhận gồm: {order_details}
Chúng tôi sẽ gọi cho quý khách để xác nhận sau ít phút nữa, quý khách vui lòng giữ máy.
Nếu có bất kì thắc mắc nào xin hãy gọi đến:
0834729504 (Khánh Trang)
0848829738 (Phú Hùng)"""
            
            send_email(subject, body, email)
            previous_orders[email] = {'confirmed': False, 'shipping': False, 'delivered': False}

        # Kiểm tra và gửi email khi đã xác nhận đơn
        if confirm_status.lower() == 'x' and not previous_orders[email]['confirmed']:
            subject = f"Đơn hàng của {name} tại 10 TIN 1 đã được xác nhận"
            body = f"Chúng tôi đã xác nhận đơn đặt hàng của quý khách, chúng tôi sẽ thông báo khi đơn hàng bắt đầu được giao đến quý khách."
            send_email(subject, body, email)
            previous_orders[email]['confirmed'] = True

        # Kiểm tra và gửi email khi đơn hàng đang giao
        if shipping_status.lower() == 'x' and not previous_orders[email]['shipping']:
            subject = f"Đơn hàng của quý khách {name} đang được giao."
            body = f"Đơn hàng của quý khách vừa hoàn thành và đang được giao đến tay quý khách. Xin cảm ơn quý khách!"
            send_email(subject, body, email)
            previous_orders[email]['shipping'] = True

        # Kiểm tra và gửi email khi đơn hàng đã giao
        if delivery_status.lower() == 'x' and not previous_orders[email]['delivered']:
            subject = f"Đơn hàng của quý khách {name} đã được giao."
            body = f"Đơn hàng của quý khách đã được giao đến tay. Xin cảm ơn!"
            send_email(subject, body, email)
            previous_orders[email]['delivered'] = True

# Chạy tool với chu kỳ 1 phút
if __name__ == '__main__':
    while True:
        print("Kiểm tra Google Sheet...")
        process_orders()
        print("Chờ 1 phút để kiểm tra tiếp...")
        time.sleep(10)  # Chờ 1 phút trước khi kiểm tra tiếp
