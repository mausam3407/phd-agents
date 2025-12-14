from langgraph.graph import StateGraph, END

from graph.state import AgentState
from graph.nodes import (
    load_profile_node,
    search_positions_node,
    match_positions_node,
)


def build_graph():
    graph = StateGraph(AgentState)

    # Register nodes
    graph.add_node("load_profile", load_profile_node)
    graph.add_node("search_positions", search_positions_node)
    graph.add_node("match_positions", match_positions_node)

    # Define edges (linear for now)
    graph.set_entry_point("load_profile")
    graph.add_edge("load_profile", "search_positions")
    graph.add_edge("search_positions", "match_positions")
    graph.add_edge("match_positions", END)

    return graph.compile()




