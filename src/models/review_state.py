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
    category: str | None
    priority: str | None
    draft_reply: str | None
    status: Status
    human_feedback: str | None
    messages: Annotated[list[AnyMessage], add_messages]