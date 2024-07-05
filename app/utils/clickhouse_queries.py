import json
import pandas as pd
from app.mongo_models import Keyword

def save_keywords_to_clickhouse(ch_db, keywords_df):
    try:
        ch_db.insert_df(
            table="keywords",
            df=keywords_df
        )
        return True
    except Exception as e:
        raise ValueError(f"Failed to save keywords to ClickHouse: {e}")
    
def keywords_by_landscape(ch_db, landscape_id):
    try:
        query = f"SELECT id FROM keywords WHERE landscape_id = {landscape_id}"
        df = ch_db.query_df(query)
        return df
    except Exception as e:
        raise ValueError(f"Failed to fetch keywords from ClickHouse: {e}")