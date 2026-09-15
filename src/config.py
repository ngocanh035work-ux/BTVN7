import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    PIPELINE_NAME = os.getenv("PIPELINE_NAME", "banking_bigquery_elt")
    
    # Source DB Config
    DB_HOST = os.getenv("SOURCE_DB_HOST")
    DB_PORT = os.getenv("SOURCE_DB_PORT")
    DB_NAME = os.getenv("SOURCE_DB_NAME")
    DB_USER = os.getenv("SOURCE_DB_USER")
    DB_PASSWORD = os.getenv("SOURCE_DB_PASSWORD")
    SOURCE_SYSTEM = os.getenv("SOURCE_SYSTEM", "CORE_BANKING")
    
    # BigQuery Config
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    BQ_PROJECT_ID = os.getenv("BQ_PROJECT_ID")
    BQ_LOCATION = os.getenv("BQ_LOCATION", "asia-southeast1")
    BQ_RAW_DATASET = os.getenv("BQ_RAW_DATASET", "banking_bronze")
    
    # Thiết lập biến môi trường cho Google SDK nhận diện tự động
    if GOOGLE_APPLICATION_CREDENTIALS:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS

    @classmethod
    def validate(cls):
        """Kiểm tra các cấu hình cốt lõi xem có bị thiếu không"""
        required_fields = ["DB_HOST", "DB_NAME", "DB_USER", "DB_PASSWORD", "BQ_PROJECT_ID"]
        missing = [field for field in required_fields if not getattr(cls, field)]
        if missing:
            raise ValueError(f"Thiếu các cấu hình bắt buộc trong file .env: {', '.join(missing)}")
