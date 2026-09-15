# Banking BigQuery ELT Pipeline (BTVN7)

Dự án cung cấp một pipeline ELT tự động bằng Python nhằm trích xuất (**Extract**) dữ liệu từ cơ sở dữ liệu nguồn PostgreSQL (Core Banking) và nạp (**Load**) toàn bộ các bảng tự động tìm thấy lên tầng Bronze (**banking_raw**) trên Google Cloud BigQuery.

## 📁 Cấu trúc thư mục (Project Structure)

Dự án được tổ chức theo mô hình module hóa gọn gàng và dễ mở rộng:

```text
BTVN7/
│
├── src/                         # Mã nguồn chính của ứng dụng
│   ├── __init__.py
│   ├── bq_load.py               # Module phụ trách nạp dữ liệu lên BigQuery (Bronze)
│   ├── config.py                # Đọc và kiểm tra tính hợp lệ của file .env
│   ├── db_connect.py            # Khởi tạo kết nối SQL và BigQuery Client
│   ├── logger.py                # Định cấu hình hệ thống Logging tập trung
│   └── sql_extract.py           # Module tự động lấy danh sách bảng và trích xuất dữ liệu
│
├── venv/                        # Môi trường ảo Python (Virtual Environment)
├── .env                         # File lưu trữ cấu hình môi trường bảo mật (Không commit)
├── .env.example                 # File cấu hình mẫu cấu trúc môi trường
├── .gitignore                   # Cấu hình bỏ qua các file nhạy cảm khi commit git
├── main.py                      # File điều phối chính (Orchestrator) của toàn bộ Pipeline
└── requirements.txt             # Danh sách các thư viện phụ thuộc cần cài đặt
```

## 🛠️ Hướng dẫn cài đặt và thiết lập

### 1. Chuẩn bị môi trường ảo
Mở terminal tại thư mục gốc `BTVN7` và khởi tạo môi trường ảo:
```bash
# Khởi tạo venv
python -m venv venv

# Kích hoạt venv (Dành cho Linux/MacOS)
source venv/bin/activate

# Kích hoạt venv (Dành cho Windows)
venv\Scripts\activate
```

### 2. Cài đặt các thư viện phụ thuộc
Cài đặt toàn bộ package cần thiết được liệt kê trong file `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 3. Cấu hình biến môi trường
Tạo file `.env` từ file mẫu `.env.example` và điền đầy đủ các thông tin kết nối hệ thống của bạn:
```bash
cp .env.example .env
```

Nội dung cấu hình trong file `.env`:
```env
PIPELINE_NAME=banking_bigquery_elt

--Cấu hình Postgre
SOURCE_DB_HOST=VM_EXTERNAL_IP
SOURCE_DB_PORT=
SOURCE_DB_NAME=core_banking
SOURCE_DB_USER=de_source_exporter
SOURCE_DB_PASSWORD=

--Cấu hình Bigquery
GOOGLE_APPLICATION_CREDENTIALS=
BQ_PROJECT_ID=
BQ_LOCATION=asia-southeast1
BQ_RAW_DATASET=banking_bronze
BQ_OPS_DATASET=banking_ops

HASH_SALT=replace-with-a-long-random-secret
SOURCE_SYSTEM=CORE_BANKING

HASH_SALT=replace-with-a-long-random-secret
SOURCE_SYSTEM=CORE_BANKING
```
*Lưu ý: Hãy chắc chắn điền ID dự án GCP vào trường `BQ_PROJECT_ID`.*

## 🚀 Cách thức vận hành

Để khởi chạy toàn bộ luồng pipeline tự động quét danh sách bảng từ Postgres nguồn, thực hiện kiểm tra chất lượng dữ liệu và nạp thẳng lên tầng Bronze của BigQuery, thực hiện lệnh duy nhất:

```bash
python main.py
```

## 📊 Tính năng cốt lõi của hệ thống

1. **Auto Table Discovery:** Hệ thống tự động truy vấn danh sách toàn bộ các bảng hiện có trong `information_schema` của PostgreSQL nguồn, loại bỏ việc khai báo cứng tên bảng thủ công.
2. **Robust Logging Engine:** Ghi nhận nhật ký tiến trình thời gian thực theo cấu trúc format pipe chuẩn chỉnh:
   `[Thời gian] | [Mức độ] | [Tên module phát log] | [Nội dung tin nhắn]`
3. **Metadata Enrichment:** Tự động tiêm thêm trường `src_system` vào cấu trúc bảng đích phục vụ cho việc truy vết nguồn gốc dữ liệu (Data Lineage) ở tầng phân tích sau này.
# BTVN7
