from fastapi import HTTPException

from langchain_core.messages import messages_to_dict
from langchain_core.runnables import RunnableConfig
from langgraph.types import Command

from src.models import generate_ticket_id
from src.nodes import build_graph

from api.schemas import TicketAction


def _build_config(
    thread_id: str,
    ticket_id: str,
    customer_id: str,
    flow: str,
    action: str | None = None,
) -> RunnableConfig:
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


class TicketService:
    def __init__(self, vectorstore, checkpointer):
        self.vectorstore = vectorstore
        self.checkpointer = checkpointer
        self.graph = None

        self._tickets: list[dict] = []
    
    def _ensure_graph(self):
        if self.graph is None:
            self.graph = build_graph(
                vectorstore=self.vectorstore,
                checkpointer=self.checkpointer
            )
    
    def create_ticket(self, ticket_content: str, customer_id: str) -> dict:
        self._ensure_graph()
        
        ticket_id = generate_ticket_id()
        
        initial_state = {
            "ticket_id": ticket_id,
            "ticket": ticket_content,
            "customer_id": customer_id,
            "messages": [],
        }
        
        config = _build_config(
            thread_id=ticket_id,
            ticket_id=ticket_id,
            customer_id=customer_id,
            flow="create",
        )
        
        result = self.graph.invoke(initial_state, config=config)
        self._tickets.append(result)
        
        return result
    
    def get_ticket_by_id(self, ticket_id: str) -> dict:
        ticket = next(
            (t for t in self._tickets if t.get("ticket_id") == ticket_id),
            None
        )
        if ticket is None:
            raise HTTPException(
                status_code=404,
                detail=f"Ticket '{ticket_id}' nie został znaleziony"
            )
        return self._serialize_ticket(ticket)
    
    def get_tickets_by_customer(self, customer_id: str) -> list[dict]:
        return [
            self._serialize_ticket(t) 
            for t in self._tickets 
            if t.get("customer_id") == customer_id
        ]
    
    def get_tickets_by_status(self, status: str) -> list[dict]:
        return [
            self._serialize_ticket(t)
            for t in self._tickets
            if t.get("status") == status
        ]
    
    def process_decision(
        self, 
        ticket_id: str, 
        action: TicketAction, 
        feedback: str
    ) -> dict:
        self._ensure_graph()
        
        ticket_index = next(
            (i for i, t in enumerate(self._tickets) if t["ticket_id"] == ticket_id),
            None
        )
        
        if ticket_index is None:
            raise HTTPException(
                status_code=404,
                detail=f"Ticket '{ticket_id}' nie został znaleziony"
            )
        
        current_ticket = self._tickets[ticket_index]
        customer_id = current_ticket.get("customer_id", "unknown")
        
        config = _build_config(
            thread_id=ticket_id,
            ticket_id=ticket_id,
            customer_id=customer_id,
            flow="decision",
            action=action.value,
        )
        
        result = self.graph.invoke(
            Command(resume={"action": action.value, "feedback": feedback}),
            config=config
        )
        
        self._tickets[ticket_index] = result
        
        return self._serialize_ticket(result)
    
    @staticmethod
    def _serialize_ticket(ticket: dict) -> dict:
        return {
            **ticket,
            "messages": messages_to_dict(ticket.get("messages", []))
        }
