from fastapi import APIRouter, File, UploadFile, Form, Depends
from ..deps import SessionDep, ClickHouseDep
from app.schemas import LandscapeCreate, Message
from typing import Annotated, Literal
import pandas as pd
from app.utils.landscape import validate_and_clean_csv, divide_chunks
from app.models import Landscape
from app.utils.clickhouse_queries import save_keywords_to_clickhouse
from app.utils.mongo_queries import save_keywords_to_mongo, keywords_by_landscape
from app.utils.sqs import SQSManager
from app.core.config import settings
import json
from app.core.mongo import get_mongo_db

router = APIRouter(
    prefix="/landscapes",
    tags=["landscapes"],
    responses={404: {"message": "Not found"}},
)

@router.post("/create", response_model=Message)
async def create_landscape(
        name: Annotated[str, Form()],
        visibility: Annotated[Literal['public', 'private', 'paid'], Form()],
        db: SessionDep,
        ch_db: ClickHouseDep,
        mongo_db = Depends(get_mongo_db),
        keyword_file: UploadFile = File(None),
        keywords: list = None
    ):

    owner_id = 1
    keywords_df = None
    serp_queue = SQSManager(settings.SERP_QUEUE_NAME)
    keyword_queue = SQSManager(settings.KEYWORD_QUEUE_NAME)

    try:
        with db.begin():
            # Save landscape metadata to database
            landscape_db = Landscape(name=name, visibility=visibility, owner_id=owner_id)
            db.add(landscape_db)
            db.flush()

            if keyword_file:
                # Validate and clean the CSV file
                keywords_df = validate_and_clean_csv(keyword_file.file)
                # add landscape_id to keywords_df
                keywords_df['landscape_id'] = landscape_db.id

            # Save keyword file to s3
            # await save_file_s3(keywords_df)
            # Save keywords to ClickHouse
            # save_keywords_to_clickhouse(ch_db, keywords_df)
            await save_keywords_to_mongo(mongo_db, keywords_df)

            keywords_list = await keywords_by_landscape(mongo_db, landscape_db.id)
            # ch_keywords_df['id'] = ch_keywords_df['id'].astype(str)

            serp_chunks = divide_chunks(keywords_list, 1000)
            # keywords_chunks = divide_chunks(ch_keywords_df, 1000)

            #serp chunks are generator objects, so we need to iterate over them
            for serp_chunk in serp_chunks:
                # Put these chunks into SERP queue
                serp_queue.send_message(json.dumps(serp_chunk['id'].tolist()))
                keyword_queue.send_message(json.dumps(serp_chunk['id'].tolist()))

            #keywords chunks are generator objects, so we need to iterate over them
            # for keyword_chunk in keywords_chunks:
            #     # Put these chunks into Keyword queue
            #     keyword_queue.send_message(json.dumps(keyword_chunk['id'].tolist()))

        return Message(message="Landscape created successfully")

    except Exception as e:
        db.rollback()
        return Message(message=f"Failed to create landscape: {e}")