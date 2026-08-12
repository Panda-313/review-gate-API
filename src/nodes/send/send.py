from langchain_core.messages import HumanMessage, AIMessage

from .schema import SendReply
from src.models import ReviewState
from src.tools import build_send_message


def send(state: ReviewState) -> SendReply:
    """
    Wysyłaj wiadomość do użytkownika korzystając z narzędzia send_message
    """
    
    send_message = build_send_message()
    
    message_to_send = state.get("draft_reply", "Domyślna wiadomość")
    
    result = send_message.invoke({"message": message_to_send})

    return {
        "messages": [
            AIMessage(content=f"Wiadomość wysłana: {result['message_sent']}")
        ],
        "status": "sent"
    }