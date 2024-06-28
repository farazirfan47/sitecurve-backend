from pydantic import BaseModel
from typing import Optional, Literal, Union
from fastapi import UploadFile

class LandscapeBase(BaseModel):
    name: str
    # owner_id: str
    visibility: str

# class KeywordObject(BaseModel):
#     name: str
#     search_engine: Literal['google', 'bing', 'yahoo']
#     device: Literal['desktop', 'mobile']
#     country: str
#     location: Optional[str] = None

class LandscapeCreate(LandscapeBase):
    # keywords: list[KeywordObject]
    keywords_file: Union[UploadFile, None] = None

class Landscape(LandscapeBase):
    id: str
    class Config:
        orm_mode = True

class Message(BaseModel):
    message: str