from graph.state import AgentState


def route_after_search(state: AgentState) -> str:
    """
    Decide what to do after searching for positions.
    """
    if not state.discovered_positions:
        if state.search_attempts < state.max_search_attempts:
            return "refine_search"
        return "end"

    return "match_positions"


def route_after_matching(state: AgentState) -> str:
    """
    Decide what to do after matching positions.
    """
    if not state.matched_positions:
        return "refine_search"

    best_score = state.matched_positions[0]["match_score"]

    if best_score < state.min_match_score:
        if state.search_attempts < state.max_search_attempts:
            return "refine_search"
        return "end"

    return "end"
