import pandas as pd
import logging
from google.cloud import bigquery
from src.config import Config

logger = logging.getLogger("pipeline.load")

class BQLoader:
    def __init__(self, bq_client):
        self.client = bq_client

    def load_to_bronze(self, df: pd.DataFrame, table_name: str, write_disposition: str = "WRITE_TRUNCATE"):
        destination_table = f"{Config.BQ_PROJECT_ID}.{Config.BQ_RAW_DATASET}.{table_name}"
        logger.info(f"Đang nạp dữ liệu lên BigQuery: {destination_table}...")
        
        job_config = bigquery.LoadJobConfig(
            write_disposition=write_disposition,
        )
        
        job = self.client.load_table_from_dataframe(df, destination_table, job_config=job_config)
        job.result()
        
        logger.info(f"THÀNH CÔNG: Đã nạp dữ liệu vào {destination_table}.")
