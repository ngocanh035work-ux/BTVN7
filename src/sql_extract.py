from typing import List
import pandas as pd
import logging
from src.config import Config

logger = logging.getLogger("pipeline.extract")

class SQLExtractor:
    def __init__(self, engine):
        self.engine = engine

    def get_all_tables(self, schema_name: str = "public") -> List[str]:
        """Tự động lấy danh sách tất cả tên bảng từ PostgreSQL nguồn"""
        logger.info(f"Đang tự động quét danh sách bảng từ schema: {schema_name}...")
        

        query = f"""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = '{schema_name}' 
              AND table_type = 'BASE TABLE';
        """
        
        try:
            with self.engine.connect() as connection:
                df_tables = pd.read_sql(query, connection)
                tables = df_tables['table_name'].tolist()
                logger.info(f"Tìm thấy tổng cộng {len(tables)} bảng trong database nguồn.")
                return tables
        except Exception as e:
            logger.error(f"Không thể lấy danh sách bảng từ PostgreSQL. Lỗi: {str(e)}")
            raise e

    def extract_table(self, table_name: str) -> pd.DataFrame:
        """Đọc toàn bộ dữ liệu từ một bảng cụ thể"""
        query = f"SELECT * FROM {table_name};"
        logger.info(f"Đang đọc dữ liệu từ bảng nguồn: {table_name}...")
        
        df = pd.read_sql(query, self.engine)
        df['src_system'] = Config.SOURCE_SYSTEM
        
        logger.info(f"Đã trích xuất thành công {len(df)} dòng.")
        return df
