from typing import cast

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from .schema import DraftUpdate, DraftResult
from src.config import BASE_NODE_MODEL, DRAFT_SYSTEM_PROMPT
from src.models import ReviewState


def draft_node(state: ReviewState) -> DraftUpdate:
    """
    Generuje draft odpowiedzi na podstawie ticketu, kategorii, priorytetu oraz feedbacku - jezeli jest podany.
    Po zakonczeniu - wszstrymuje proces i czeka na feedback od użytkownika
    """

    llm = ChatOpenAI(model=BASE_NODE_MODEL, temperature=0)
    structured_llm = llm.with_structured_output(DraftResult)

    human_message = (
            f"Kategoria: {state.get('category')}\n"
            f"Priorytet: {state.get('priority')}\n\n"
            f"Zgłoszenie klienta:\n{state['ticket']}"
        ) if not state.get("feedback") else (
            f"Kategoria: {state.get('category')}\n"
            f"Priorytet: {state.get('priority')}\n\n"
            f"Zgłoszenie klienta:\n{state['ticket']}\n\n"
            f"Ostatni draft:\n{state['draft_reply']}\n\n"
            f"Feedback managera (obowiazkowo uwzglednij):\n{state['feedback']}\n\n"
            "Przygotuj nowa wersje draftu po poprawkach."
        )


    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=DRAFT_SYSTEM_PROMPT),
        HumanMessage(content=human_message),
    ])

    result: DraftResult = cast(DraftResult, structured_llm.invoke(prompt.format_messages()))

    return {
        "draft_reply": result.draft_reply,
        "status": "waiting_human",
        "messages": [
            AIMessage(content=f"Wygenerowano draft:\n\n{result.draft_reply}")
        ]
    }

    if action == "reject":
        return {
            "draft_reply": result.draft_reply,
            "status": "rejected",
            "messages": [
                AIMessage(content=f"Wygenerowano draft:\n\n{result.draft_reply}"),
                HumanMessage(content=f"Odrzucono. Powód: {feedback}"),
            ]
        }

    return {
        "draft_reply": feedback if feedback else result.draft_reply,
        "status": "waiting_human",
        "messages": [
            AIMessage(content=f"Wygenerowano draft:\n\n{result.draft_reply}"),
            HumanMessage(content="Zatwierdzono." + (f" Poprawka: {feedback}" if feedback else "")),
        ]
    }
