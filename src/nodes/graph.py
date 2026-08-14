from functools import partial

from langchain_community.vectorstores import Chroma
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph

from .history import history
from .send import send
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

    if status == "rejected":
        return END

    return "send"

def build_graph(vectorstore: Chroma, checkpointer=None):
    if checkpointer is None:
        checkpointer = InMemorySaver()
    
    builder = StateGraph(ReviewState)

    builder.add_node("history", history)
    builder.add_node("classify", classify_node)
    builder.add_node("draft", partial(draft_node, vectorstore=vectorstore))
    builder.add_node("human_approval", human_approval)
    builder.add_node("send", send)

    builder.add_edge(START, "classify")
    builder.add_edge("classify", "history")
    builder.add_edge("history", "draft")
    builder.add_edge("draft", "human_approval")

    builder.add_conditional_edges(
        "human_approval",
        route_after_approval,
    )

    builder.add_edge("send", END)

    return builder.compile(checkpointer=checkpointer)
