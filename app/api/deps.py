from ..core.db import SessionLocal
from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session
from ..core.clickhouse import clickhouse_manager
import clickhouse_connect

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SessionDep = Annotated[Session, Depends(get_db)]

def get_ch_db():
    client = clickhouse_manager.get_client()
    try:
        yield client
    finally:
        clickhouse_manager.disconnect()

ClickHouseDep = Annotated[clickhouse_connect.driver.Client, Depends(get_ch_db)]