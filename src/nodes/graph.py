from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph

from .human_approval import human_approval
from .draft import draft_node
from .classify import classify_node
from src.models import ReviewState

def route_after_approval(state: ReviewState) -> str:
    """
    Decyduje, dokąd iść po decyzji człowieka.
    """
    status = state.get("status")

    if status == "drafting":
        return "draft"

    return END

def build_graph():
    builder = StateGraph(ReviewState)

    builder.add_node("classify", classify_node)
    builder.add_node("draft", draft_node)
    builder.add_node("human_approval", human_approval)

    builder.add_edge(START, "classify")
    builder.add_edge("classify", "draft")
    builder.add_edge("draft", "human_approval")

    builder.add_conditional_edges(
        "human_approval",
        route_after_approval,
    )

    checkpointer = InMemorySaver()

    return builder.compile(checkpointer=checkpointer)
