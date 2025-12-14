from langgraph.graph import StateGraph, END

from graph.state import AgentState
from graph.nodes import (
    load_profile_node,
    search_positions_node,
    match_positions_node,
    refine_search_node,
)
from graph.edges import (
    route_after_search,
    route_after_matching,
)


def build_graph():
    graph = StateGraph(AgentState)

    # Nodes
    graph.add_node("load_profile", load_profile_node)
    graph.add_node("search_positions", search_positions_node)
    graph.add_node("match_positions", match_positions_node)
    graph.add_node("refine_search", refine_search_node)

    # Entry
    graph.set_entry_point("load_profile")

    # Flow
    graph.add_edge("load_profile", "search_positions")

    graph.add_conditional_edges(
        "search_positions",
        route_after_search,
        {
            "match_positions": "match_positions",
            "refine_search": "refine_search",
            "end": END,
        },
    )

    graph.add_edge("refine_search", "search_positions")

    graph.add_conditional_edges(
        "match_positions",
        route_after_matching,
        {
            "refine_search": "refine_search",
            "end": END,
        },
    )

    return graph.compile()
