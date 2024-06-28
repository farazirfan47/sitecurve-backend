from fastapi import APIRouter, File, UploadFile, Form
from ..deps import SessionDep
from app.schemas import LandscapeCreate, Message
from typing import Annotated, Literal
import pandas as pd
from app.utils.landscape import validate_and_clean_csv, save_file_s3
from app.models import Landscape

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
        keyword_file: UploadFile = File(None),
        keywords: list = None
    ):

    owner_id = "8cb99a81-39a8-46fc-81c8-8ae6ae6b4fc0"

    try:
        with db.begin():
            # Save landscape metadata to database
            landscape_db = Landscape(name=name, visibility=visibility, owner_id=owner_id)
            db.add(landscape_db)
            db.flush()

            if keyword_file:
                # Validate and clean the CSV file
                keyword_file_name = validate_and_clean_csv(keyword_file.file, landscape_db.id)

            # Save keyword file to s3
            await save_file_s3(keyword_file_name)

        return Message(message="Landscape created successfully")

    except Exception as e:
        db.rollback()
        return Message(message=f"Failed to create landscape: {e}")