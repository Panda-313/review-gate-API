import json

from langchain_core.messages import AIMessage

from src.config import HISTORY_PATH
from .schema import HistoryReply
from src.models import ReviewState


def history(state: ReviewState) -> HistoryReply:
    """
    Sprawdza historie uzytkownika. I jeżeli istnieje, to ustawia pole history
    """

    customer_id = state["customer_id"]

    with open(HISTORY_PATH, "r", encoding="utf-8") as file:
        history = json.load(file)
        try:
            tickets = history[customer_id]["tickets"]
            history_of_customer = ", ".join(
                f"Pytanie: {ticket['ticket']}, udzielona odpowiedz: {ticket['final_reply']}"
                for ticket in tickets
            )
        except KeyError:
            print(f"{customer_id} nie istnieje.")
            history_of_customer = ""

    return {
        "customer_history": history_of_customer,
        "messages": [
            AIMessage(content=f"Znaleziono historie uzytkownika: {history_of_customer}")
        ]
    }