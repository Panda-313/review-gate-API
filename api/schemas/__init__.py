from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from src.models.review_state import Status

class TicketAction(str, Enum):
    APPROVE = "approve"
    REJECT = "reject"
    EDIT = "edit"
    MANUAL_EDIT = "manual_edit"


class TicketCreateRequest(BaseModel):
    ticket: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Treść zgłoszenia od klienta",
        examples=["Nie mogę zalogować się do panelu. Dostaję błąd 403."]
    )
    customer_id: str = Field(
        ...,
        min_length=1,
        pattern=r"^cust_[a-zA-Z0-9]+$",
        description="ID klienta w formacie cust_XXX",
        examples=["cust_001"]
    )


class TicketDecisionRequest(BaseModel):
    action: TicketAction = Field(
        ...,
        description="Akcja do wykonania na tickecie"
    )
    feedback: str = Field(
        default="",
        max_length=2000,
        description="Opcjonalny feedback/komentarz"
    )


class TicketCreateResponse(BaseModel):
    ticket_id: str
    status: Status


class TicketResponse(BaseModel):
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
    messages: list[dict[str, Any]] = Field(default_factory=list)


class TicketSummaryResponse(BaseModel):
    ticket_id: str
    status: Status
    final_reply: str | None = None
