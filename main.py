from pprint import pprint

from dotenv import load_dotenv

from src.cli import run_review_loop
from src.nodes import build_graph

load_dotenv()

graph = build_graph()

initial_state = {
    "ticket": "Nie mogę zalogować się do panelu. Dostaję błąd 403 od rana.",
    "messages": [],
    "id": '001'
}
config = {
    "configurable": {
        "thread_id": initial_state["id"]
    }
}

result = run_review_loop(graph=graph, initial_state=initial_state, config=config)

print("Wynik stanu:")
pprint(result)
