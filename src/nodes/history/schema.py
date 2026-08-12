from typing import TypedDict, NotRequired

from langchain_core.messages import AnyMessage

class HistoryReply(TypedDict):
    messages: NotRequired[list[AnyMessage]]
    customer_history: NotRequired[str]