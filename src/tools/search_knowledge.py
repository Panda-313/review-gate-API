from typing import Any

from langchain_core.tools import tool


def build_search_knowledge(vectorstore: Any):
    @tool("search_knowledge", description="""
    Przeszukuje wewnętrzną bazę wiedzy supportu (dokumentacja, procedury, FAQ) 
i zwraca najbardziej relevantne fragmenty pasujące do zapytania.

Używaj tego toola zawsze przed napisaniem draftu odpowiedzi, 
szczególnie gdy zgłoszenie dotyczy logowania, konta, płatności, 
subskrypcji, API, integracji lub problemów technicznych.

Wejście: krótkie zapytanie opisujące problem klienta 
(np. treść ticketa, kategoria + główny objaw).

Wyjście: 2–4 najbardziej pasujące fragmenty wiedzy 
wraz z tytułem artykułu źródłowego.""")
    def search_knowledge(query: str):
        print("TOOL CALLED")
        results = vectorstore.similarity_search_with_score(query, k=3)

        if not results:
            return "Brak wynikow w dokumentach"

        formatted_results: list[str] = []
        for index, (doc, _) in enumerate(results, start=1):
            formatted_results.append(
                f"[{index}]: {doc.page_content}"
            )

        print("ZWROCONO : ", formatted_results)
        return "\n\n".join(formatted_results)


    return search_knowledge


