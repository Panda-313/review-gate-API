from contextlib import asynccontextmanager
from typing import Any, Literal

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import messages_to_dict
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from pydantic import BaseModel

from src.models.review_state import ReviewStateBase, generate_ticket_id
from src.utils import load_vectorstore
from src.nodes import build_graph

Action = Literal["approve", "reject", "manual_edit", "edit"]


class TicketRequest(BaseModel):
    ticket: str
    customer_id: str


class TicketCreateResponse(BaseModel):
    ticket_id: str
    status: str


class TicketDecisionRequest(BaseModel):
    action: str
    feedback: str


class UserTicketResponse(BaseModel):
    status: str


class UserFinalTickerResponse(UserTicketResponse):
    reply: str


class AdminTicketResponse(ReviewStateBase):
    messages: list[dict[str, Any]] = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    app.state.vectorstore = load_vectorstore()
    app.state.checkpointer = InMemorySaver()
    app.state.all_tickets = []
    try:
        yield
    finally:
        if hasattr(app.state, "vectorstore"):
            del app.state.vectorstore
        if hasattr(app.state, "checkpointer"):
            del app.state.checkpointer


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get('/ticket/{ticket_id}', response_model=AdminTicketResponse)
def get_ticket(ticket_id: str):
    all_tickets = app.state.all_tickets
    ticket = next(
        (ticket for ticket in all_tickets if ticket.get("ticket_id") == ticket_id), None
    )

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return {**ticket, "messages": messages_to_dict(ticket.get("messages", []))}


@app.get('/tickets/{customer_id}', response_model=list[AdminTicketResponse])
def get_customer_tickets(customer_id: str):
    customer_tickets = [
        ticket for ticket in app.state.all_tickets
        if ticket["customer_id"] == customer_id
    ]
    return [
        {**ticket, "messages": messages_to_dict(ticket.get("messages", []))}
        for ticket in customer_tickets
    ]


@app.post("/ticket", response_model=TicketCreateResponse)
def create_ticket(request: TicketRequest) -> TicketCreateResponse:
    vectorstore = app.state.vectorstore
    checkpointer = app.state.checkpointer

    app.state.graph = build_graph(vectorstore=vectorstore, checkpointer=checkpointer)

    ticket_id = generate_ticket_id()

    initial_state = {
        "ticket_id": ticket_id,
        "ticket": request.ticket,
        "customer_id": request.customer_id,
        "messages": [],
    }

    app.state.config = {
        "configurable": {
            "thread_id": ticket_id,
        }
    }

    try:
        result = app.state.graph.invoke(initial_state, config=app.state.config)
        app.state.all_tickets.append(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return TicketCreateResponse(ticket_id=ticket_id, status="in_progress")


@app.get("/tickets-waiting", response_model=list[AdminTicketResponse])
def tickets_waiting():
    waiting_tickets = [
        ticket for ticket in app.state.all_tickets
        if ticket.get("status") == "waiting_human"
    ]
    return [
        {**ticket, "messages": messages_to_dict(ticket.get("messages", []))}
        for ticket in waiting_tickets
    ]


@app.post("/tickets/{ticket_id}/decision", response_model=AdminTicketResponse)
def ticket_decision(ticket_id: str, decision: TicketDecisionRequest):
    ticket_index = next(
        (
            i for i, ticket in enumerate(app.state.all_tickets)
            if ticket["ticket_id"] == ticket_id
        ),
        None,
    )

    if ticket_index is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket = app.state.all_tickets[ticket_index]

    config = {
        "configurable": {
            "thread_id": ticket["ticket_id"]
        }
    }

    result = app.state.graph.invoke(Command(resume={
        "action": decision.action,
        "feedback": decision.feedback
    }), config=config)

    app.state.all_tickets[ticket_index] = result

    return {**result, "messages": messages_to_dict(result.get("messages", []))}
