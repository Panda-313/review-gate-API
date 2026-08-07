from typing import cast

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from .schema import DraftUpdate, DraftResult
from src.config import BASE_NODE_MODEL, DRAFT_SYSTEM_PROMPT
from src.models import ReviewState


def draft_node(state: ReviewState) -> DraftUpdate:
    """
    Generuje draft odpowiedzi na podstawie ticketu, kategorii i priorytetu.
    """

    llm = ChatOpenAI(model=BASE_NODE_MODEL, temperature=0)
    structured_llm = llm.with_structured_output(DraftResult)

    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=DRAFT_SYSTEM_PROMPT),
        HumanMessage(content=(
            f"Kategoria: {state.get('category')}\n"
            f"Priorytet: {state.get('priority')}\n\n"
            f"Zgłoszenie klienta:\n{state['ticket']}"
        )),
    ])

    result: DraftResult = cast(DraftResult, structured_llm.invoke(prompt.format_messages()))

    return {
        "draft_reply": result.draft_reply,
        "status": "waiting_human",
        "messages": [
            AIMessage(content=f"Wygenerowano draft opowiedzi: \n\n{result.draft_reply}"),
        ]
    }