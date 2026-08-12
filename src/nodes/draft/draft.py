from typing import Any, cast

from langchain_community.vectorstores import Chroma
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from .schema import DraftUpdate, DraftResult
from src.config import BASE_NODE_MODEL, DRAFT_SYSTEM_PROMPT
from src.models import ReviewState
from src.tools import build_search_knowledge


def draft_node(state: ReviewState, vectorstore: Chroma) -> DraftUpdate:
    """
    Generuje draft odpowiedzi na podstawie ticketu, kategorii, priorytetu oraz feedbacku - jezeli jest podany.
    Po zakonczeniu - wszstrymuje proces i czeka na feedback od użytkownika
    """

    llm = ChatOpenAI(model=BASE_NODE_MODEL, temperature=0)
    structured_llm = llm.with_structured_output(DraftResult)

    search_query = f"{state.get('category')} - {state.get('ticket')}"
    search_knowledge = build_search_knowledge(vectorstore)
    knowledge_context = search_knowledge.func(search_query)

    knowledge_section = ""
    if knowledge_context is not None:
        knowledge_section = f"\n\nWyniki z bazy wiedzy:\n{_format_knowledge_context(knowledge_context)}"

    print("*" * 60)
    print(knowledge_section)
    print("*" * 60)

    human_message = (
            "Przygotuj odpowiedź do klienta na podstawie danych poniżej.\n\n"
            f"Kategoria:\n{state.get('category')}\n\n"
            f"Priorytet:\n{state.get('priority')}\n\n"
            f"Zgłoszenie klienta:\n{state['ticket']}"
            f"{knowledge_section}\n\n"
            f"Historia zapytan dla naszego uzytkownika: {state['customer_history']} \n\n"
            "Ważne: jeśli są dostępne wyniki z bazy wiedzy, oprzyj odpowiedź przede wszystkim na nich. "
            "Ważne: jeśli użytkownik zadał już w przeszłości podobne pytanie - zbuduj odpowiedź wzorując sie na naszej odpowiedzi na jego uprzednio zadane pytanie. "
            "Jeśli baza wiedzy wskazuje konkretne przyczyny problemu albo sugeruje konkretne pytania diagnostyczne, użyj właśnie ich."
        ) if not state.get("feedback") else (
            "Przygotuj nową wersję draftu na podstawie danych poniżej.\n\n"
            f"Kategoria:\n{state.get('category')}\n\n"
            f"Priorytet:\n{state.get('priority')}\n\n"
            f"Zgłoszenie klienta:\n{state['ticket']}"
            f"{knowledge_section}\n\n"
            f"Ostatni draft:\n{state['draft_reply']}\n\n"
            f"Historia zapytan dla naszego uzytkownika: {state['customer_history']} \n\n"
            f"Feedback managera (obowiazkowo uwzglednij):\n{state['feedback']}\n\n"
            "Ważne: jeśli są dostępne wyniki z bazy wiedzy, oprzyj odpowiedź przede wszystkim na nich. "
            "Ważne: jeśli użytkownik zadał już w przeszłości podobne pytanie - zbuduj odpowiedź wzorując sie na naszej odpowiedzi na jego uprzednio zadane pytanie. "
            "Uwzględnij każdy punkt feedbacku managera i użyj konkretnych informacji z bazy wiedzy zamiast ogólników. "
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


def _format_knowledge_context(knowledge_context: Any) -> str:
    if knowledge_context is None:
        return "Brak wyników."

    if isinstance(knowledge_context, str):
        return knowledge_context

    return str(knowledge_context)
