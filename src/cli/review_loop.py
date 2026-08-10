from langgraph.types import Command

import questionary


def run_review_loop(graph, initial_state: dict, config: dict):
    result = graph.invoke(initial_state, config=config)

    while True:
        snapshot = graph.get_state(config)
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
        elif human_decision == "Odrzuc":
            resume_value = {
                "action": "reject",
                "feedback": input("\nPodaj powod odrzucenia")
            }
        elif human_decision == "Edytuj Manualnie":
            resume_value = {
                "action": "manual_edit",
                "feedback": input("\nPodaj poprawiona wiadomosc")
            }
        else:
            resume_value = {
                "action": "edit",
                "feedback": input("\nPodaj feedback do wiadomosci ktory zostanie uwzlgedniony przy generowaniu nowej\n")
            }

        result = graph.invoke(Command(resume=resume_value), config=config)

    return result
