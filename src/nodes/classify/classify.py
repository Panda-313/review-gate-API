from typing import cast

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.config import BASE_NODE_MODEL, CLASSIFY_SYSTEM_PROMPT
from src.models import ReviewState
from .schema import ClassificationResult


def classify_node(state: ReviewState) -> dict:
    """
    Node, który analizuje ticket i ustawia category + priority.
    Zwraca tylko te klucze, które chce zaktualizować w stanie.
    """
    llm = ChatOpenAI(model=BASE_NODE_MODEL, temperature=0)

    structured_llm = llm.with_structured_output(ClassificationResult)

    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=CLASSIFY_SYSTEM_PROMPT),
        HumanMessage(content=f"Zgłoszenie klienta: \n\n{state['ticket']}"),
    ])

    result = cast(ClassificationResult, structured_llm.invoke(prompt.format_messages()))

    return {
        "category": result.category,
        "priority": result.priority,
        "status": "classified",
        "messages": [
            AIMessage(
                content=f"Sklasyfikowano: category={result.category}, "
                        f"priority={result.priority}. "
                        f"Uzasadnienie: {result.reasoning}"
            )
        ]

    }