from typing import cast

from langchain_core.messages import HumanMessage
from langgraph.types import interrupt

from .schema import HumanApproval
from src.models import ReviewState


def human_approval(state: ReviewState) -> HumanApproval:
    """
       Generuje finalna wersje odpowiedzi
       """
    human_decision = interrupt({
        "draft": state['draft_reply'],
    })

    action = human_decision.get("action", "approve")
    feedback = human_decision.get("feedback")

    if action == "reject":
        return {
            "final_reply": cast(str, state['draft_reply']),
            "status": "rejected",
            "messages": [
                HumanMessage(content=f"Odrzucono draft. Powód: {feedback}")
            ],
        }

    if action == "manual_edit":
        return {
            "final_reply": feedback,
            "status": "approved",
            "messages": [
                HumanMessage(content=f"Zatwierdzono po ręcznej edycji: {feedback}")
            ],
        }

    if action == "approve":
        return {
            "final_reply": cast(str, state['draft_reply']),
            "status": "approved",
            "messages": [
                HumanMessage(content="Zatwierdzono draft bez zmian.")
            ],
        }

    return {
        "final_reply": "",
        "status": "drafting",
        "feedback": feedback,
        "messages": [
            HumanMessage(content=f"Poproś o poprawki draftu: {feedback}")
        ],
    }
