from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class ApplicationDraft(BaseModel):
    position_id: str
    email: Optional[str] = None
    sop: Optional[str] = None
    created_at: datetime = datetime.utcnow()
