from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# -------------------------
# Core State Components
# -------------------------

class ProfileState(BaseModel):
    """Structured representation of the user's academic profile."""
    name: str
    education: str
    research_interests: List[str]
    skills: List[str]
    preferences: Dict[str, Any]


class PositionState(BaseModel):
    """Raw PhD position information extracted from the web."""
    id: str
    title: str
    supervisor: Optional[str] = None
    institution: Optional[str] = None
    description: str
    url: str
    country: Optional[str] = None
    deadline: Optional[str] = None
    funding: Optional[str] = None


class MatchedPositionState(PositionState):
    """PhD position after relevance scoring."""
    match_score: float = Field(..., ge=0.0, le=1.0)
    match_explanation: List[str]


class DraftState(BaseModel):
    """Generated application material."""
    position_id: str
    email_draft: Optional[str] = None
    sop_draft: Optional[str] = None
    last_updated: Optional[str] = None


# -------------------------
# LangGraph Global State
# -------------------------

class AgentState(BaseModel):
    """
    Global state passed between LangGraph nodes.
    This should NEVER contain non-serializable objects.
    """

    # Profile
    profile: Optional[ProfileState] = None

    # Positions
    discovered_positions: List[PositionState] = Field(default_factory=list)
    matched_positions: List[MatchedPositionState] = Field(default_factory=list)

    # Drafts
    drafts: List[DraftState] = Field(default_factory=list)

    # Control & bookkeeping
    current_step: str = "start"
    errors: List[str] = Field(default_factory=list)
    approved: bool = False

    # Metadata (safe for debugging / logging)
    metadata: Dict[str, Any] = Field(default_factory=dict)

