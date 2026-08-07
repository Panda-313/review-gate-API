from typing import NotRequired, TypedDict

from langchain_core.messages import AnyMessage
from pydantic import BaseModel, Field

from src.models.review_state import Status

class DraftResult(BaseModel):
    draft_reply: str = Field(description="Profesjonalna, empatyczna odpowiedź, która zostanie zwrócona do użytkownika")

class DraftUpdate(TypedDict):
    draft_reply: NotRequired[str]
    status: NotRequired[Status]
    messages: NotRequired[list[AnyMessage]]