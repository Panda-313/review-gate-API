from typing import TypedDict, NotRequired

from langchain_core.messages import AnyMessage

from src.models.review_state import Status


class HumanApproval(TypedDict):
    final_reply: NotRequired[str]
    status: Status
    feedback: NotRequired[str]
    messages: NotRequired[list[AnyMessage]]
