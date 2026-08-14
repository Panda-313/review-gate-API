from typing import TypedDict, Annotated, Literal
import uuid

from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages
from pydantic import BaseModel

Status = Literal[
    "drafting",
    "waiting_human",
    "approved",
    "rejected",
    "sent"
]


def generate_ticket_id() -> str:
    return f"ticket_{uuid.uuid4().hex[:8]}"


class ReviewStateBase(BaseModel):
    ticket_id: str
    ticket: str
    customer_id: str
    category: str | None = None
    priority: str | None = None
    draft_reply: str | None = None
    feedback: str | None = None
    final_reply: str | None = None
    customer_history: str | None = None
    status: Status = "drafting"


class ReviewState(TypedDict):
    ticket_id: str
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