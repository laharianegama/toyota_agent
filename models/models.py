from typing import Optional, Union
from pydantic import BaseModel, Field

class Query(BaseModel):
    query: str = Field(..., example="I want to book a test drive")

class QueryResponse(BaseModel):
    message: str = Field(..., example="Response message for the user")
    