from typing import Optional, List
from pydantic import BaseModel, Field, validator


class PhDPosition(BaseModel):
    """
    Structured PhD position extracted from the web.
    """

    id: str = Field(description="Unique hash or slug")
    title: str
    description: str
    url: str

    supervisor: Optional[str] = None
    institution: Optional[str] = None
    country: Optional[str] = None

    deadline: Optional[str] = None
    funding: Optional[str] = None
    requirements: List[str] = Field(default_factory=list)

    @validator("title", "description", "url")
    def must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Field cannot be empty")
        return v
