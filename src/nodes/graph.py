from langgraph.constants import START, END
from langgraph.graph import StateGraph

from .draft import draft_node
from .classify import classify_node
from src.models import ReviewState


def build_graph():
    builder = StateGraph(ReviewState)

    builder.add_node("classify", classify_node)
    builder.add_node("draft", draft_node)

    builder.add_edge(START, "classify")
    builder.add_edge("classify", "draft")
    builder.add_edge("draft", END)

    return builder.compile()