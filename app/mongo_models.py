from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from pydantic.types import Literal
from datetime import datetime

PyObjectId = Annotated[str, BeforeValidator(str)]


class Serp(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    rank_group: int = Field(...)
    rank_absolute: int = Field(...)
    title: str = Field(...)
    description: str = Field(...)
    url: str = Field(...)
    breadcrumb: str = Field(...)
    website_type: Optional[str] = Field(None)
    business_model: Optional[str] = Field(None)
    content_parse_status: Literal["PENDING", "DONE", "FAILED"] = Field("PENDING")
    openai_tag_status: Literal["PENDING", "DONE", "FAILED"] = Field("PENDING")
    created_at: datetime
    updated_at: datetime

  
class Keyword(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    landscape_id: int = Field(...)
    keyword: str = Field(...)
    search_engine: str = Field(...)
    device: str = Field(...)
    country: str = Field(...)
    location: Optional[str] = Field(None)
    search_volume: Optional[int] = Field(None)
    cpc: Optional[float] = Field(None)
    competition: Optional[float] = Field(None)
    low_top_of_page_bid: Optional[float] = Field(None)
    high_top_of_page_bid: Optional[float] = Field(None)
    serps: Optional[list[Serp]] = Field([])
    serp_api_status: Literal["PENDING", "DONE", "FAILED"] = Field("PENDING")
    keyword_api_status: Literal["PENDING", "DONE", "FAILED"] = Field("PENDING")
    openai_tag_status: Literal["PENDING", "DONE", "FAILED"] = Field("PENDING")
    created_at: datetime
    updated_at: datetime