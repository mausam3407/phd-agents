from graph.graph import build_graph
from graph.state import AgentState

if __name__ == "__main__":
    graph = build_graph()

    initial_state = AgentState()
    final_state = graph.invoke(initial_state)

    print("Final step:", final_state.current_step)
    print("Errors:", final_state.errors)
    print("Matches:", len(final_state.matched_positions))
