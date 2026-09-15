from sqlalchemy import create_engine
from google.cloud import bigquery
from src.config import Config

def get_sql_engine():
    connection_string = f"postgresql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"
    return create_engine(connection_string)

def get_bq_client():
    return bigquery.Client(project=Config.BQ_PROJECT_ID, location=Config.BQ_LOCATION)
