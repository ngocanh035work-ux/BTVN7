import os
import sys
import logging
from datetime import datetime

def setup_logging(level: str = "INFO") -> None:
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        

    log_filename = f"{log_dir}/pipeline_{datetime.now().strftime('%Y%m%d')}.log"
    

    log_format = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    
    # 4. Thiết lập cấu hình ghi đồng thời ra cả Màn hình và File
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),                         
            logging.FileHandler(log_filename, encoding="utf-8")         
        ],
        force=True,
    )
