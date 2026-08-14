from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request

from api.schemas import (
    TicketCreateRequest,
    TicketCreateResponse,
    TicketDecisionRequest,
    TicketResponse,
)
from api.services import TicketService

router = APIRouter(
    prefix="/tickets",
    tags=["tickets"],
)

def get_ticket_service(request: Request) -> TicketService:
    return request.app.state.ticket_service


TicketServiceDep = Annotated[TicketService, Depends(get_ticket_service)]

@router.post(
    "",
    response_model=TicketCreateResponse,
    status_code=201,
    summary="Utwórz nowy ticket",
    description="Tworzy nowy ticket i rozpoczyna proces review."
)
def create_ticket(
    request: TicketCreateRequest,
    service: TicketServiceDep
) -> TicketCreateResponse:
    result = service.create_ticket(
        ticket_content=request.ticket,
        customer_id=request.customer_id
    )
    return TicketCreateResponse(
        ticket_id=result["ticket_id"],
        status=result["status"]
    )


@router.get(
    "/{ticket_id}",  # GET /tickets/{ticket_id}
    response_model=TicketResponse,
    summary="Pobierz ticket po ID"
)
def get_ticket(
    ticket_id: str,
    service: TicketServiceDep
) -> TicketResponse:
    return service.get_ticket_by_id(ticket_id)


@router.get(
    "",
    response_model=list[TicketResponse],
    summary="Lista ticketów"
)
def list_tickets(
    service: TicketServiceDep,
    customer_id: str | None = Query(
        default=None,
        description="Filtruj po ID klienta"
    ),
    status: str | None = Query(
        default=None,
        description="Filtruj po statusie (np. waiting_human)"
    )
) -> list[TicketResponse]:

    if customer_id:
        tickets = service.get_tickets_by_customer(customer_id)
    elif status:
        tickets = service.get_tickets_by_status(status)
    else:
        tickets = [
            service._serialize_ticket(t) 
            for t in service._tickets
        ]
    
    return tickets


@router.post(
    "/{ticket_id}/decision",
    response_model=TicketResponse,
    summary="Podjęcie decyzji o tickecie"
)
def submit_decision(
    ticket_id: str,
    decision: TicketDecisionRequest,
    service: TicketServiceDep
) -> TicketResponse:
    return service.process_decision(
        ticket_id=ticket_id,
        action=decision.action,
        feedback=decision.feedback
    )
