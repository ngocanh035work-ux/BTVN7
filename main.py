import sys
import logging
from src.config import Config
from src.logger import setup_logging
from src.db_connect import get_sql_engine, get_bq_client
from src.sql_extract import SQLExtractor
from src.bq_load import BQLoader

def main():
    setup_logging("INFO")
    logger = logging.getLogger("pipeline_main")
    logger.info(f"=== KHỞI CHẠY PIPELINE TỰ ĐỘNG: {Config.PIPELINE_NAME} ===")
    
    try:
        Config.validate()
    except ValueError as e:
        logger.error(f"Lỗi cấu hình môi trường: {e}")
        sys.exit(1)

    logger.info("Đang khởi tạo các kết nối cơ sở dữ liệu...")
    sql_engine = get_sql_engine()
    bq_client = get_bq_client()

    extractor = SQLExtractor(engine=sql_engine)
    loader = BQLoader(bq_client=bq_client)

    try:
        tables_to_migrate = extractor.get_all_tables(schema_name="public")
    except Exception:
        sys.exit(1)


    for table in tables_to_migrate:
        logger.info(f"TIẾN TRÌNH XỬ LÝ BẢNG: {table} <<<")
        try:
            df_extracted = extractor.extract_table(table)
            loader.load_to_bronze(df_extracted, table_name=table)
            
        except Exception as e:
            logger.error(f"Thất bại nghiêm trọng tại bảng {table}. Chi tiết: {str(e)}")
            continue

    logger.info(f"=== HOÀN THÀNH TOÀN BỘ PIPELINE: {Config.PIPELINE_NAME} ===")

if __name__ == "__main__":
    main()
