from typing import TypedDict, Annotated, Literal

from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages

Status = Literal[
    "drafting",
    "waiting_human",
    "approved",
    "rejected",
    "sent"
]

class ReviewState(TypedDict):
    ticket: str
    customer_id: str
    category: str | None
    priority: str | None
    draft_reply: str | None
    feedback: str | None
    final_reply: str | None
    customer_history: str | None
    status: Status
    messages: Annotated[list[AnyMessage], add_messages]