import clickhouse_connect
import os
from dotenv import load_dotenv


load_dotenv()

client = clickhouse_connect.get_client(
        host=os.getenv("CH_HOST"),
        user=os.getenv("CH_USER"),
        password=os.getenv("CH_PASSWORD"),
        secure=True,
        verify='proxy'
    )

# Function to create a table in ClickHouse
def create_table(table_name, columns, pk):
    # Construct the column definitions
    column_defs = ", ".join([f"{name} {dtype}" for name, dtype in columns.items()])
    
    # SQL query to create the table
    query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        {column_defs}
    ) ENGINE = MergeTree()
    PRIMARY KEY {pk}
    """
    
    # Execute the query
    client.query(query)
    print(f"Table '{table_name}' created successfully.")

# Example table definitions
tables = {
    "keywords": {
        "id": "UUID DEFAULT generateUUIDv4()",
        "landscape_id": "Int",
        "keyword": "String",
        "search_engine": "String",
        "device": "String",
        "country": "String",
        "search_volume": "Nullable(Int)",
        "cpc": "Nullable(Float)",
        "competition": "Nullable(Float)",
        "low_top_of_page_bid": "Nullable(Float)",
        "high_top_of_page_bid": "Nullable(Float)",
        "serp_api_status": "Bool Default false",
        "keyword_api_status": "Bool Default false",
        "openai_api_status" : "Bool Default false",
        "created_at": "DateTime DEFAULT now()",
        "updated_at": "DateTime DEFAULT now()"
    },
    "serps": {
        "id": "UUID DEFAULT generateUUIDv4()",
        "landscape_id": "Int",
        "keyword_id": "UUID",
        "rank_group": "Int",
        "rank_absolute": "Int",
        "title": "String",
        "description": "String",
        "url": "String",
        "breadcrumb": "String",
        "content_parse_status": "String Default 'P'",
        "created_at": "DateTime DEFAULT now()",
        "updated_at": "DateTime DEFAULT now()"
    }
}

# Create the tables
for table_name, columns in tables.items():
    create_table(table_name, columns, "landscape_id")