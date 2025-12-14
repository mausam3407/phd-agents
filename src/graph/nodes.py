from pathlib import Path
from typing import List

from graph.state import AgentState
from agents.profile_agent import ProfileAgent
from agents.matching_agent import MatchingAgent
from schemas.position import PhDPosition
from agents.search_agent import SearchAgent


# -------------------------
# Node: Load Profile
# -------------------------

def load_profile_node(state: AgentState) -> AgentState:
    """
    Loads and validates the user profile.
    """
    agent = ProfileAgent(Path("data/profile"))
    profile = agent.build_profile()

    state.profile = profile
    state.current_step = "profile_loaded"
    return state


# -------------------------
# Node: Match Positions
# -------------------------

def match_positions_node(state: AgentState) -> AgentState:
    """
    Matches discovered positions against the profile.
    """
    if state.profile is None:
        state.errors.append("Profile not loaded")
        return state

    if not state.discovered_positions:
        state.errors.append("No positions available for matching")
        return state

    matcher = MatchingAgent()
    results = matcher.match(
        profile=state.profile,
        positions=state.discovered_positions
    )

    # Convert to state-compatible format
    state.matched_positions = [
        {
            **r.position.model_dump(),
            "match_score": r.score,
            "match_explanation": r.explanation,
        }
        for r in results
    ]

    state.current_step = "positions_matched"
    return state


def search_positions_node(state: AgentState) -> AgentState:
    """
    Discovers PhD positions using SearchAgent.
    """
    if state.profile is None:
        state.errors.append("Profile not loaded before search")
        return state

    agent = SearchAgent()
    positions = agent.discover(state.profile)

    state.discovered_positions = positions
    state.current_step = "positions_discovered"
    return state
