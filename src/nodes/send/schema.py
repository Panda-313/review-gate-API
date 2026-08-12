from typing import TypedDict, NotRequired

from langchain_core.messages import AnyMessage

from src.models.review_state import Status


class SendReply(TypedDict):
    messages: NotRequired[list[AnyMessage]]
    status: Status