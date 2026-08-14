from langgraph.types import Command

import questionary


def _build_config(
    thread_id: str,
    ticket_id: str,
    customer_id: str,
    flow: str,
    action: str | None = None,
) -> dict:
    tags = [f"flow:{flow}", f"customer:{customer_id}"]
    if action:
        tags.append(f"action:{action}")
    
    return {
        "configurable": {"thread_id": thread_id},
        "tags": tags,
        "metadata": {
            "ticket_id": ticket_id,
            "customer_id": customer_id,
            "flow": flow,
            "action": action,
        },
    }


def run_review_loop(graph, initial_state: dict, config: dict):
    ticket_id = initial_state.get("ticket_id", "unknown")
    customer_id = initial_state.get("customer_id", "unknown")
    
    langsmith_config = _build_config(
        thread_id=config["configurable"]["thread_id"],
        ticket_id=ticket_id,
        customer_id=customer_id,
        flow="create",
    )
    
    result = graph.invoke(initial_state, config=langsmith_config)

    while True:
        snapshot = graph.get_state(langsmith_config)
        if not snapshot.tasks or not snapshot.tasks[0].interrupts:
            break

        interrupt_value = snapshot.tasks[0].interrupts[0].value
        print("\nAktualny draft:\n")
        print(interrupt_value["draft"])

        human_decision = questionary.select("Czy podoba Ci sie przygotowany draft?", [
            "Zaakcteptuj",
            "Odrzuc",
            "Edytuj",
            "Edytuj Manualnie",
        ]).ask()

        if human_decision == "Zaakcteptuj":
            resume_value = {
                "action": "approve",
                "feedback": None
            }
            action = "approve"
        elif human_decision == "Odrzuc":
            resume_value = {
                "action": "reject",
                "feedback": input("\nPodaj powod odrzucenia\n")
            }
            action = "reject"
        elif human_decision == "Edytuj Manualnie":
            resume_value = {
                "action": "manual_edit",
                "feedback": input("\nPodaj poprawiona wiadomosc\n")
            }
            action = "manual_edit"
        else:
            resume_value = {
                "action": "edit",
                "feedback": input("\nPodaj feedback do wiadomosci ktory zostanie uwzlgedniony przy generowaniu nowej\n")
            }
            action = "edit"

        decision_config = _build_config(
            thread_id=config["configurable"]["thread_id"],
            ticket_id=ticket_id,
            customer_id=customer_id,
            flow="decision",
            action=action,
        )
        
        result = graph.invoke(Command(resume=resume_value), config=decision_config)

    return result
