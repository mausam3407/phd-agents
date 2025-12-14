from typing import List, Dict, Optional
from pydantic import BaseModel, Field, validator


class Education(BaseModel):
    degree: str
    field: str
    institution: str
    thesis_title: Optional[str] = None
    thesis_keywords: List[str] = Field(default_factory=list)


class Profile(BaseModel):
    """
    Canonical user profile schema.
    This should be stable across the entire system.
    """

    name: str
    education: Education

    research_interests: List[str]
    skills: List[str]

    preferences: Dict[str, str] = Field(
        default_factory=dict,
        description="User constraints like country, stipend, field"
    )

    @validator("research_interests", "skills")
    def non_empty_lists(cls, v):
        if not v:
            raise ValueError("List cannot be empty")
        return v
