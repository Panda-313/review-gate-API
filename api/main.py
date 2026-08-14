from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langgraph.checkpoint.memory import InMemorySaver

from src.utils import load_vectorstore

from api.routers import tickets_router
from api.services import TicketService


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    
    vectorstore = load_vectorstore()
    checkpointer = InMemorySaver()
    
    app.state.ticket_service = TicketService(
        vectorstore=vectorstore,
        checkpointer=checkpointer
    )
    
    try:
        yield
    finally:
        pass


app = FastAPI(
    title="Review Gate API",
    description="API do zarządzania ticketami wsparcia z AI review",
    version="0.1.0",
    lifespan=lifespan,
)


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


app.include_router(tickets_router)

@app.get(
    "/health",
    tags=["health"],
    summary="Health check"
)
def health_check():
    return {"status": "healthy"}
