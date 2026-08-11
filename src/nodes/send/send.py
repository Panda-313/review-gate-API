from langchain_core.messages import HumanMessage

from .schema import SendReply
from src.models import ReviewState


def send(state: ReviewState) -> SendReply:
    """
    Wyslij wiadomosc do uzytkownika
    """

    return {
        "messages": [
            HumanMessage("Wiadomosc zostala wyslana do uzytkownika")
        ]
    }