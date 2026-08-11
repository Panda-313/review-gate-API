from typing import TypedDict, NotRequired

from langchain_core.messages import AnyMessage

class SendReply(TypedDict):
    messages: NotRequired[list[AnyMessage]]