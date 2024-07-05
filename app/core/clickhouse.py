import clickhouse_connect
from ..core.config import settings

class ClickHouseConnectionManager:
    def __init__(self, host: str, username: str, password: str):
        self.host = host
        self.username = username
        self.password = password
        self.client = None

    def connect(self):
        if self.client is None:
            self.client = clickhouse_connect.get_client(
                host=self.host,
                user=self.username,
                password=self.password,
                secure=True,
                verify='proxy'
            )

    def disconnect(self):
        if self.client is not None:
            self.client.close()
            self.client = None

    def get_client(self):
        if self.client is None:
            self.connect()
        return self.client

# Configuration for the database connection
db_config = {
    "host": settings.CH_HOST,
    "username": settings.CH_USER,
    "password": settings.CH_PASSWORD,
}

clickhouse_manager = ClickHouseConnectionManager(**db_config)