from pprint import pprint

from dotenv import load_dotenv

from src.cli import run_review_loop
from src.nodes import build_graph
from src.utils import load_vectorstore
from src.models import generate_ticket_id

load_dotenv()

vectorstore = load_vectorstore()
graph = build_graph(vectorstore=vectorstore)

ticket_id = generate_ticket_id()
customer_id = 'cust_001'

initial_state = {
    "ticket_id": ticket_id,
    "ticket": "Nie mogę zalogować się do panelu. Dostaję błąd 403 od rana.",
    "messages": [],
    "customer_id": customer_id
}
config = {
    "configurable": {
        "thread_id": customer_id
    }
}

result = run_review_loop(graph=graph, initial_state=initial_state, config=config)

print("Wynik stanu:")
pprint(result)
