from pprint import pprint

from dotenv import load_dotenv

from src.nodes import build_graph

load_dotenv()

graph = build_graph()

initial_state = {
    "ticket": "Nie mogę zalogować się do panelu. Dostaję błąd 403 od rana.",
    "messages": []
}

result = graph.invoke(initial_state)

print("Wynik stanu:")
pprint(result)
